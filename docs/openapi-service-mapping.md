# OpenAPI to frontend service mapping

Issue #3 maps the frontend service boundary to `openapi.yaml`.

| Mock service operation | HTTP operation |
| --- | --- |
| `signIn` | `GET /auth/google/login`, `GET /auth/google/callback` |
| `currentSession` / `signOut` | `GET /session`, `DELETE /session` |
| `listBoards` / `createBoard` | `GET /boards`, `POST /boards` |
| `getBoard` / `renameBoard` | `GET /boards/{boardId}`, `PATCH /boards/{boardId}` |
| `openBoard` | `POST /boards/{boardId}/open` |
| `archiveBoard` / `restoreBoard` | `POST /boards/{boardId}/archive`, `POST /boards/{boardId}/restore` |
| `listTasks` / `createTask` | `GET /boards/{boardId}/tasks`, `POST /boards/{boardId}/tasks` |
| `updateTask` / `deleteTask` | `PATCH /boards/{boardId}/tasks/{taskId}`, `DELETE /boards/{boardId}/tasks/{taskId}` |
| `moveTask` | `PATCH /boards/{boardId}/tasks/{taskId}/status` |
| `search` | `GET /search/tasks` |

Protected operations use the `tidyboard_session` cookie. Missing and foreign
resources share the `unavailable` response. Task update, move, and delete
operations require the observed version; stale writes return `409` with latest
content and never upsert deleted tasks. Archived boards retain task operations.

Validate from `frontend/` with:

```bash
npm run validate:openapi
```
