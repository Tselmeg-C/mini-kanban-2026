from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Cookie, Depends, FastAPI, Header, HTTPException, Query, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

SESSION_COOKIE = "tidyboard_session"
CSRF_COOKIE = "tidyboard_csrf"
UNAVAILABLE = {"code": "unavailable", "message": "Resource is unavailable."}


def now() -> datetime:
    return datetime.now(timezone.utc)


class Session(BaseModel):
    name: str
    email: str


class BoardInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)

    @field_validator("name")
    @classmethod
    def trim_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Board name must be 1-120 characters.")
        return value


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=5000)

    @field_validator("title")
    @classmethod
    def trim_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Task title must be 1-120 characters.")
        return value


class TaskUpdate(TaskCreate):
    status: str
    version: int = Field(ge=1)


class StatusUpdate(BaseModel):
    status: str
    version: int = Field(ge=1)


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    description: str
    status: str
    created_at: datetime = Field(alias="createdAt")
    version: int


class BoardSummary(BaseModel):
    id: str
    name: str
    archived: bool
    opened_at: datetime = Field(alias="openedAt")
    task_count: int = Field(alias="taskCount")


class Board(BoardSummary):
    tasks: list[Task]


class SearchResult(Task):
    board_id: str = Field(alias="boardId")
    board_name: str = Field(alias="boardName")
    archived: bool


class Store:
    def __init__(self) -> None:
        self.boards: dict[str, dict] = {}
        self.sessions: dict[str, dict] = {}
        self.next_board = 1
        self.next_task = 1

    def create_session(self, subject: str, name: str = "Google user", email: str = "user@example.test") -> tuple[str, str]:
        token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(24)
        self.sessions[token] = {"subject": subject, "session": Session(name=name, email=email), "csrf": csrf, "expires_at": now() + timedelta(hours=1)}
        return token, csrf

    def identity(self, token: str | None) -> dict:
        session = self.sessions.get(token or "")
        if not session or session["expires_at"] < now():
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"code": "unauthenticated", "message": "Sign in required."})
        return session

    def board(self, subject: str, board_id: str) -> dict:
        board = self.boards.get(board_id)
        if not board or board["owner"] != subject:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=UNAVAILABLE)
        return board

    def task(self, subject: str, board_id: str, task_id: str) -> tuple[dict, dict]:
        board = self.board(subject, board_id)
        task = next((item for item in board["tasks"] if item["id"] == task_id), None)
        if not task:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=UNAVAILABLE)
        return board, task


store = Store()
app = FastAPI(title="TidyBoard API", version="0.1.0")


@app.exception_handler(HTTPException)
async def http_error(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.detail if isinstance(exc.detail, dict) else {"code": "error", "message": str(exc.detail)})


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, __: RequestValidationError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"code": "validation", "message": "Invalid request."})


def current_session(tidyboard_session: Annotated[str | None, Cookie()] = None) -> dict:
    return store.identity(tidyboard_session)


def csrf(session: Annotated[dict, Depends(current_session)], tidyboard_csrf: Annotated[str | None, Cookie()] = None, x_csrf_token: Annotated[str | None, Header()] = None) -> dict:
    if not tidyboard_csrf or not x_csrf_token or not hmac.compare_digest(tidyboard_csrf, x_csrf_token) or not hmac.compare_digest(session["csrf"], x_csrf_token):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail={"code": "csrf", "message": "CSRF token required."})
    return session


SessionDep = Annotated[dict, Depends(current_session)]
CsrfDep = Annotated[dict, Depends(csrf)]


def board_view(board: dict) -> Board:
    tasks = sorted(board["tasks"], key=lambda item: (item["created_at"], item["id"]))
    return Board(id=board["id"], name=board["name"], archived=board["archived"], openedAt=board["opened_at"], taskCount=len(tasks), tasks=[task_view(task) for task in tasks])


def task_view(task: dict) -> Task:
    return Task(id=task["id"], title=task["title"], description=task["description"], status=task["status"], createdAt=task["created_at"], version=task["version"])


def error_conflict(task: dict) -> HTTPException:
    return HTTPException(status.HTTP_409_CONFLICT, detail={"code": "conflict", "message": "This task changed. Review the latest saved version.", "latest": task_view(task).model_dump(mode="json", by_alias=True)})


@app.get("/auth/google/login", response_class=RedirectResponse, status_code=302)
def google_login() -> RedirectResponse:
    if not os.getenv("GOOGLE_CLIENT_ID") or not os.getenv("GOOGLE_REDIRECT_URI"):
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail={"code": "oauth_unconfigured", "message": "Google sign-in is not configured."})
    return RedirectResponse("https://accounts.google.com/o/oauth2/v2/auth", status_code=302)


@app.get("/auth/google/callback")
def google_callback(code: str = Query(...), state: str = Query(...)) -> RedirectResponse:
    if not code or not state or not os.getenv("GOOGLE_CLIENT_ID") or not os.getenv("GOOGLE_CLIENT_SECRET"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"code": "validation", "message": "Invalid sign-in callback."})
    raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"code": "oauth_unavailable", "message": "Google token exchange is not configured."})


@app.get("/session", response_model=Session)
def get_session(session: SessionDep) -> Session:
    return session["session"]


@app.delete("/session", status_code=204)
def sign_out(response: Response, session: CsrfDep, tidyboard_session: Annotated[str, Cookie()]) -> None:
    store.sessions.pop(tidyboard_session, None)
    response.delete_cookie(SESSION_COOKIE)
    response.delete_cookie(CSRF_COOKIE)


@app.get("/boards", response_model=list[BoardSummary])
def list_boards(session: SessionDep, include_archived: Annotated[bool, Query(alias="includeArchived")] = True) -> list[BoardSummary]:
    boards = [board for board in store.boards.values() if board["owner"] == session["subject"] and (include_archived or not board["archived"])]
    return [BoardSummary(id=b["id"], name=b["name"], archived=b["archived"], openedAt=b["opened_at"], taskCount=len(b["tasks"])) for b in sorted(boards, key=lambda item: (-item["opened_at"].timestamp(), item["id"]))]


@app.post("/boards", response_model=Board, status_code=201)
def create_board(body: BoardInput, session: CsrfDep) -> Board:
    board = {"id": f"b{store.next_board}", "owner": session["subject"], "name": body.name, "archived": False, "opened_at": now(), "tasks": []}
    store.next_board += 1; store.boards[board["id"]] = board
    return board_view(board)


@app.get("/boards/{board_id}", response_model=Board)
def get_board(board_id: str, session: SessionDep) -> Board: return board_view(store.board(session["subject"], board_id))


@app.patch("/boards/{board_id}", response_model=Board)
def rename_board(board_id: str, body: BoardInput, session: CsrfDep) -> Board:
    board = store.board(session["subject"], board_id); board["name"] = body.name; return board_view(board)


def mutate_board(board_id: str, session: CsrfDep, archived: bool) -> Board:
    board = store.board(session["subject"], board_id); board["archived"] = archived; board["opened_at"] = now() if not archived else board["opened_at"]; return board_view(board)


@app.post("/boards/{board_id}/open", response_model=Board)
def open_board(board_id: str, session: CsrfDep) -> Board:
    board = store.board(session["subject"], board_id); board["opened_at"] = now(); return board_view(board)


@app.post("/boards/{board_id}/archive", response_model=Board)
def archive_board(board_id: str, session: CsrfDep) -> Board: return mutate_board(board_id, session, True)


@app.post("/boards/{board_id}/restore", response_model=Board)
def restore_board(board_id: str, session: CsrfDep) -> Board: return mutate_board(board_id, session, False)


@app.get("/boards/{board_id}/tasks", response_model=list[Task])
def list_tasks(board_id: str, session: SessionDep) -> list[Task]: return [task_view(task) for task in sorted(store.board(session["subject"], board_id)["tasks"], key=lambda item: (item["created_at"], item["id"]))]


@app.post("/boards/{board_id}/tasks", response_model=Task, status_code=201)
def create_task(board_id: str, body: TaskCreate, session: CsrfDep) -> Task:
    board = store.board(session["subject"], board_id)
    task = {"id": f"t{store.next_task}", "title": body.title, "description": body.description, "status": "todo", "created_at": now(), "version": 1}
    store.next_task += 1; board["tasks"].append(task); return task_view(task)


@app.get("/boards/{board_id}/tasks/{task_id}", response_model=Task)
def get_task(board_id: str, task_id: str, session: SessionDep) -> Task: return task_view(store.task(session["subject"], board_id, task_id)[1])


def check_version(task: dict, version: int) -> None:
    if task["version"] != version: raise error_conflict(task)


def check_status(value: str) -> str:
    if value not in {"todo", "doing", "done"}: raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"code": "validation", "message": "Choose a valid status."})
    return value


@app.patch("/boards/{board_id}/tasks/{task_id}", response_model=Task)
def update_task(board_id: str, task_id: str, body: TaskUpdate, session: CsrfDep) -> Task:
    _, task = store.task(session["subject"], board_id, task_id); check_version(task, body.version); task.update(title=body.title, description=body.description, status=check_status(body.status), version=task["version"] + 1); return task_view(task)


@app.delete("/boards/{board_id}/tasks/{task_id}", status_code=204)
def delete_task(board_id: str, task_id: str, version: Annotated[int, Query(ge=1)], session: CsrfDep) -> None:
    board, task = store.task(session["subject"], board_id, task_id); check_version(task, version); board["tasks"].remove(task)


@app.patch("/boards/{board_id}/tasks/{task_id}/status", response_model=Task)
def move_task(board_id: str, task_id: str, body: StatusUpdate, session: CsrfDep) -> Task:
    _, task = store.task(session["subject"], board_id, task_id); check_version(task, body.version); task.update(status=check_status(body.status), version=task["version"] + 1); return task_view(task)


@app.get("/search/tasks", response_model=list[SearchResult])
def search_tasks(session: SessionDep, q: str = Query(..., min_length=1), page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100, alias="pageSize")) -> list[SearchResult]:
    needle = q.strip().casefold()
    if not needle: return []
    matches = []
    for board in store.boards.values():
        if board["owner"] != session["subject"]: continue
        for task in board["tasks"]:
            if needle in f"{task['title']} {task['description']}".casefold():
                matches.append(SearchResult(**task_view(task).model_dump(by_alias=True), boardId=board["id"], boardName=board["name"], archived=board["archived"]))
    matches.sort(key=lambda item: (-item.created_at.timestamp(), item.id))
    start = (page - 1) * page_size
    return matches[start:start + page_size]
