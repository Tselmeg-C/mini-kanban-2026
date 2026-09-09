# Mini Kanban

Issue #2 currently contains a dependency-free frontend prototype backed by a
development-only in-memory mock service. No real Google authentication, API, or
durable storage is included yet.

## Run

```bash
cd frontend
npm test
npm run test:browser
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
