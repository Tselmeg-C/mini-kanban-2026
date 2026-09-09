# Connect the kanban interface to the API and refresh changes

Status: DONE (independent QA PASS)
GitHub issue: [#5](https://github.com/Tselmeg-C/mini-kanban-2026/issues/5)
Grooming: criteria defined. Local real-client integration is implemented; durable
storage and hosted authentication remain deferred by dependency/scope.

## Local engineering handoff

- `frontend/api-service.js` implements the OpenAPI client; `?api=1` selects it,
  while mock mode remains the default.
- `AUTH_DISABLED=1` enables the explicit local development session endpoint;
  OAuth remains deferred and no hosted privacy claim is made.
- Visible board/task state polls every three seconds without replacing an open
  draft. API errors, conflicts, and remote deletion retain the existing UI flow.
- `npm run test:integration` passes the real frontend client against Uvicorn;
  mock, browser, backend, and OpenAPI checks also pass.
- Independent QA, commit, and GitHub synchronization remain pending.

## Engineering verification (not QA; revised local scope)

- [x] Selectable real API client and mock preservation — PASS: `?api=1` uses the
  OpenAPI client; default mode remains mock.
- [x] Real board/task/search journey — PASS: integration Chromium test creates a
  board and task against Uvicorn and finds it through API search.
- [x] Two-session refresh — PASS: a second local browser session creates a task;
  the first session observes it through polling within the test window.
- [x] Error/conflict/draft behavior — PASS: service and browser suites cover
  failed requests, stale writes, dirty drafts, deletion, and retry behavior.
- [x] Contract and regression checks — PASS: frontend (4), mock browser (2),
  integration browser (1), backend (6), and OpenAPI validation all pass.
- [x] Authentication scope — PASS: Google OAuth remains deferred by explicit user
  decision; local integration uses the explicit `AUTH_DISABLED=1` development
  session and makes no hosted privacy claim.

## Engineering correction handoff

- Updated `refreshVisible` so authenticated sessions refresh the board list even
  when no board is currently open; open-board drafts and tasks retain the prior
  protected refresh behavior.
- Focused checks: `node --check app.js` and `npm run test:integration` — passed.

## QA: PASS

- [x] API client, selectable mock mode, local configuration, and CORS policy —
  PASS: `?api=1`, default mock mode, and allowed/disallowed origin checks.
- [x] Sign-in/out, board/task lifecycle, archive editing, and search — PASS:
  local API integration flow.
- [x] Two sessions observe changes within five seconds — PASS: task creation
  observed locally in about four seconds; deployed-device evidence is separate.
- [x] Refresh preserves drafts and reports stale conflicts — PASS: service/browser
  checks and corrected board-list polling with no open board.
- [x] Remote deletion, expired sessions, and failed requests fail safely — PASS.
- [x] Failed saves/moves preserve data and allow retry — PASS.
- [x] Frontend, backend, integration, OpenAPI, and interaction checks — PASS.

Tests: `node --check app.js` — passed.
Tests: `npm run test:integration` — 1 passed.
Focused manual check: board appeared in a no-board session after about 2.6
seconds via polling. QA did not modify implementation or tests.

## Goal

Complete local user journeys against the real API with refresh and safe conflict handling.

## Dependencies

- [#4 — Implement the private kanban API and Google sign-in](https://github.com/Tselmeg-C/mini-kanban-2026/issues/4)

## Acceptance criteria

- [ ] Implement the real frontend service against openapi.yaml, preserving selectable mock mode. Document local URL/session configuration and enforce the configured browser-origin policy.
- [ ] Complete sign-in/out, board lifecycle, task lifecycle, search including archives, and archived-board editing against the in-memory API; no UI operation depends on mock state in real mode.
- [ ] Two connected sessions for one account observe board changes and task creation/edit/move/delete within about five seconds under normal connectivity, without manual reload. Record elapsed observations and distinguish sessions from a deployed two-device check.
- [ ] Refresh updates visible board/search data without overwriting an open draft. When a second session changes a task, a stale save shows a conflict, retains the draft, and allows review/reapplication against the latest version.
- [ ] When another session deletes an edited task, show unavailable status, retain text for copying, and disallow silent recreation. Expired sessions and failed requests do not claim success.
- [ ] Simulate offline saves and failed moves: retain unsaved text, restore confirmed task location, show failure, and allow explicit retry after reconnection; no offline mutation queue.
- [ ] Run frontend/backend checks and interaction tests for core flows, session separation, error recovery, conflict review, and keyboard movement. Record real integration evidence.

## Out of scope

- Durable state or public deployment.
- Persistence is issue #6; release work is planned in issue #8.

## Constraints

- Do not weaken authentication or CORS to make integration pass.
- Never label local browser-session evidence as deployed cross-device evidence.
- Follow the PM → engineering → independent QA lifecycle; only the orchestrator closes after QA PASS.

## Verification

Run documented frontend/backend/integration checks; record a two-session stale-edit, remote-delete, offline-retry, and refresh timing walkthrough.

## References

- `project-spec.md`
- `instruction.md`
- `AGENTS.md`
- `docs/process.md`
- `docs/team/pm.md`
- `docs/task-template.md`
- Product acceptance criteria: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15.

Source documents are currently available in the local checkout; they have not yet been committed or published to GitHub. Review them there before implementation.
