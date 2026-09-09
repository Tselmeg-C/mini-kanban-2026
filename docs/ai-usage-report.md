# AI usage report

## Issue #1 — product assumptions and implementation plan

- Tool: Codex; Ponytail skill used to keep the planning change focused.
- User task: “lets proceed with the first issue”.
- Work: read canonical GitHub issue #1 and local product/process/backlog documents;
  retain existing minor defaults with explicit assumption labels; write the
  implementation plan, all-16-criterion mapping, prerequisites, and phase gates;
  reconcile `instruction.md` with the canonical `project-spec.md` filename and
  separately tracked release scope.
- No subagents, application implementation, credential inspection, or cloud setup.
- Human review: not yet performed on these changes.
- Independent QA: pending; engineering review is not a QA PASS.
- Limitations: no running app exists. Real Google authentication, browser tests,
  persistence, and physical cross-device evidence belong to later issues.

## Issue #2 — mock frontend

- Tool: Codex; Ponytail skill used to avoid a framework and build pipeline.
- Work: created a native HTML/CSS/JavaScript frontend, one mock service boundary,
  representative seed data, validation/conflict behavior, and Node built-in tests.
- Human review and independent QA: pending.
- Limitations: browser/manual accessibility and interaction verification remain
  to be performed; the sandbox also blocks binding a local HTTP server; the mock
  session makes no authentication claim.

QA follow-up: service and static-server checks pass, but browser/manual QA is
FAIL/pending because this environment has no browser automation. The issue stays
open until keyboard, focus, drag/drop, dirty-panel, responsive, and visual-state
checks are run independently.

Browser QA: Playwright and Chromium were installed with user authorization;
`npm run test:browser` passed the core journey, dirty-draft, deletion, archive,
and restore checks. Full browser matrix and scale checks remain issue #7 work.

## Issue #3 — OpenAPI contract

- Work: defined `openapi.yaml` for session, board, task, status, and search
  operations; documented ownership, unavailable-resource behavior, versions,
  conflicts, refresh timing, and service mapping.
- Validation: `npm run validate:openapi` passes with 18 operations.
- QA PASS: operation, security, error, status, and conflict assertions passed.

## Issue #4 — FastAPI backend

- Work: added a temporary in-memory FastAPI API with opaque sessions, CSRF
  protection, ownership isolation, board/task lifecycle, search, validation,
  version conflicts, and safe unconfigured Google OAuth endpoints.
- Validation: `uv run python -m unittest discover -s tests -v` passes 6 tests;
  OpenAPI validation continues to pass.
- Limitation: no authorized Google OAuth credentials or second external account
  were available, so real provider verification remains incomplete.

Scope update: the user explicitly deferred authentication from this project
milestone. OAuth setup and private hosted workspaces are now release follow-up
work rather than a blocker for the local API milestone.

QA PASS for the revised local scope: six backend tests, OpenAPI validation, code
compilation, and Uvicorn startup smoke passed. OAuth remains deferred.

## Issue #5 — real API client

- Work: added a selectable OpenAPI client, explicit local dev session, CORS
  configuration, three-second visible-state polling, and real-client browser
  integration coverage.
- Validation: mock tests (4), Chromium mock tests (2), integration browser test
  (1), backend tests (6), and OpenAPI validation all pass.
- Independent QA: pending.

QA PASS for the revised local scope: mock, Chromium, real-client integration,
backend, and OpenAPI checks all pass; OAuth remains deferred.

## Issue #6 — SQLite persistence

- Work: replaced the process-local board/task store with a stdlib SQLite store,
  added `DATABASE_PATH` configuration and repeatable schema setup, persisted all
  board/task mutations, and isolated tests with disposable databases.
- Validation: 7 backend tests (including restart persistence and stale-write /
  delete checks), mock tests (4), Chromium tests (2), real-client integration
  (1), and OpenAPI validation pass.
- Limitation: sessions remain in memory because authentication is intentionally
  deferred for this local milestone.

## Issue #7 — local user journeys and setup

- Work: ran clean frontend/backend installs, all service/browser/API/contract
  checks, and documented each of the 16 product criteria with evidence and
  release gaps. Added `.env.example`, corrected the README, and isolated the
  API browser test with a disposable SQLite database after QA exposed stale
  local data affecting repeatability.
- Validation: `npm ci`, `uv sync`, backend 7 tests, frontend 4 tests, Chromium
  2 tests, API integration 1 test, and OpenAPI validation pass.
- Limitations: hosted Google OAuth, physical/public-device evidence, other
  browsers, and the full 20-by-200 visual scale run remain release follow-ups.

## Independent QA backfill

- A separate QA pass audited each engineering handoff for issues #1–#7 without
  modifying implementation, tests, or docs.
- Verdicts: #1 PARTIAL, #2 PARTIAL, #3 PASS, #4 PASS for approved local scope,
  #5 PARTIAL, #6 PARTIAL, and #7 FAIL. Evidence and reopened issue actions are
  recorded in `docs/qa/independent-handoff-audit.md`.
