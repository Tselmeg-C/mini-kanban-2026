# OpenAPI to frontend service mapping

Issue #3 maps the frontend service boundary to `openapi.yaml`.

| Mock service operation | HTTP operation |
| --- | --- |
| `signIn` | `POST /dev/session` (local development only) |
| `currentSession` / `signOut` | `GET /session`, `DELETE /session` |
| `listBoards` / `createBoard` | `GET /boards`, `POST /boards` |
| `getBoard` / `renameBoard` | `GET /boards/{boardId}`, `PATCH /boards/{boardId}` |
| `openBoard` | `POST /boards/{boardId}/open` |
| `archiveBoard` / `restoreBoard` | `POST /boards/{boardId}/archive`, `POST /boards/{boardId}/restore` |
| `listTasks` / `createTask` | `GET /boards/{boardId}/tasks`, `POST /boards/{boardId}/tasks` |
| `updateTask` / `deleteTask` | `PATCH /boards/{boardId}/tasks/{taskId}`, `DELETE /boards/{boardId}/tasks/{taskId}` |
| `moveTask` | `PATCH /boards/{boardId}/tasks/{taskId}/status` |
| `search` | `GET /search/tasks` |

External authentication is outside this project; `/dev/session` is enabled only
with `AUTH_DISABLED=1`. Protected operations use the `tidyboard_session` cookie.
Missing and foreign
resources share the `unavailable` response. Task update, move, and delete
operations require the observed version; stale writes return `409` with latest
content and never upsert deleted tasks. Archived boards retain task operations.

Validate from `frontend/` with:

```bash
npm run validate:openapi
```
