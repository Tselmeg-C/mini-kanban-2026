# TidyBoard API

This is the issue #4 temporary in-memory FastAPI backend. It has no automatic
seed users or demo authentication. Tests create explicit identities through the
test-only store helper; production authentication is Google OAuth only.

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
uv run python -m unittest discover -s tests -v
```

Google authentication is deferred from this project milestone. The login and
callback endpoints remain safe unconfigured stubs; no credentials are needed or
included. The temporary store is local development infrastructure only and will
be replaced by SQLite in issue #6.

For the local real-client walkthrough, run `AUTH_DISABLED=1 uv run uvicorn
app.main:app --reload`, then open `http://localhost:4173/?api=1`. The development
session endpoint is disabled unless `AUTH_DISABLED=1` is explicitly set.
