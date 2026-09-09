# TidyBoard API

This is the local FastAPI backend. Boards and tasks persist in SQLite at
`DATABASE_PATH` (default `backend/tidyboard.sqlite3`); the schema is created on
startup and the local database is ignored by Git. Tests use disposable SQLite
files and create explicit identities through the test-only store helper.

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
uv run python -m unittest discover -s tests -v
```

Google authentication is deferred from this project milestone. The login and
callback endpoints remain safe unconfigured stubs; no credentials are needed or
included.

For the local real-client walkthrough, run `AUTH_DISABLED=1 uv run uvicorn
app.main:app --reload`, then open `http://localhost:4173/?api=1`. The development
session endpoint is disabled unless `AUTH_DISABLED=1` is explicitly set.
