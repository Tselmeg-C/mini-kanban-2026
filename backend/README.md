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
