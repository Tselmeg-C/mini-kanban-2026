# TidyBoard

Issue #2 currently contains a dependency-free frontend prototype backed by a
development-only in-memory mock service. No real Google authentication, API, or
durable storage is included yet.

## Run

```bash
cd frontend
npm test
npm run test:browser
npm run validate:openapi
python3 -m http.server 4173
```

Open <http://localhost:4173>. Choose the mock Google sign-in, open a seeded
board, and exercise task creation, editing, status changes, drag-and-drop,
archive/restore, deletion, and search. The service boundary lives in
`frontend/service.js`; UI code does not call HTTP directly.

## Current verification

`npm test` runs the Node built-in test runner against validation, lifecycle,
search, archive, deletion, and stale-edit behavior. `npm run test:browser`
launches Chromium through Playwright for the core mock journey and archive flow.
`npm run validate:openapi` validates the root API contract before backend work.

## Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
uv run python -m unittest discover -s tests -v
```

The backend currently uses an explicit temporary in-memory store. Google OAuth
configuration names are documented in `backend/README.md`; without credentials,
the OAuth endpoints fail safely and do not create a session.
