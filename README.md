# TidyBoard

TidyBoard is a desktop-first kanban workspace with a dependency-light frontend,
FastAPI backend, and local SQLite persistence. Google authentication and hosted
cross-device privacy are release follow-up work; local development uses an
explicit mock identity.

## Run

```bash
cd frontend
npm ci
npm test
npm run test:browser
npm run test:integration
npm run test:scale
npm run validate:openapi
npm start
```

Open <http://localhost:4173>. Choose the development mock sign-in, create a
board, add and edit a task, move it with the status selector or drag-and-drop,
archive/restore the board, delete the task, and search for it. The service
boundary lives in `frontend/service.js` and `frontend/api-service.js`; UI code
does not call HTTP directly.

## Current verification

`npm test` runs the Node built-in test runner against validation, lifecycle,
search, archive, deletion, and stale-edit behavior. `npm run test:browser`
launches Chromium through Playwright for the core mock journey and archive flow.
`npm run validate:openapi` validates the root API contract before backend work.
`npm run test:integration` starts the API with `AUTH_DISABLED=1` and a
disposable `DATABASE_PATH`, then checks the real frontend client against it.

## Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
uv run python -m unittest discover -s tests -v
```

Google OAuth configuration names are documented in `backend/README.md`; without
credentials, the OAuth endpoints fail safely and do not create a session.

## Configuration

Copy `.env.example` for local reference. `DATABASE_PATH` selects the SQLite
file (default `backend/tidyboard.sqlite3`), `FRONTEND_ORIGIN` controls CORS,
and `AUTH_DISABLED=1` enables the local development session endpoint. Never put
credentials in `.env` or commit that file.

To exercise the real frontend client locally, start the backend with
`AUTH_DISABLED=1` and open <http://localhost:4173/?api=1>. Mock mode remains the
default. The local API client uses `http://localhost:8000` unless
`localStorage.tidyboard-api-url` overrides it.
