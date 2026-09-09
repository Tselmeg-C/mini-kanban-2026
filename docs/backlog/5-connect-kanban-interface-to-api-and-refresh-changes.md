# Connect the kanban interface to the API and refresh changes

Status: IN PROGRESS (independent QA PARTIAL; reopened)
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

## Independent QA handoff

**PARTIAL (2026-09-09):** real client, mock mode, local two-session refresh,
errors, and integration pass. Polling stops when no board is open, so board-list
changes are not refreshed there; hosted cross-device evidence is absent. The
formal QA report is recorded on this issue.

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
