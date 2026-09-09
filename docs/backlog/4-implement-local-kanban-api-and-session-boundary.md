# Implement the local kanban API and session boundary

Status: IN PROGRESS (scope correction; QA pending)
GitHub issue: [#4](https://github.com/Tselmeg-C/mini-kanban-2026/issues/4)
Grooming: criteria defined. The user removed Google OAuth and all external
authentication from the project design; local mock sessions are the complete
authentication scope.

## Local engineering handoff

- `backend/` contains the FastAPI app, temporary in-memory store, lifecycle
  routes, search, and version conflicts. Session/authentication work is deferred.
- `uv run python -m unittest discover -s tests -v` passes 6 endpoint tests.
- `npm run validate:openapi` passes the root contract with 17 operations.
- External sign-in, hosted privacy, and public account isolation are outside the
  project and must not be presented as completed.

## Engineering verification (not QA; revised local scope)

- [x] FastAPI app and temporary store — PASS: backend test suite passed 6 tests.
- [x] Session expiry, sign-out boundary, CSRF, validation, lifecycle, search,
  and stale-write behavior — PASS: `uv run python -m unittest discover -s tests -v`.
- [x] Ownership behavior within the explicit test-session boundary — PASS: foreign
  board/task reads and search return unavailable/empty results.
- [x] Contract and startup — PASS: `npm run validate:openapi` reports 17 operations;
  `/openapi.json` returned HTTP 200 from Uvicorn.
- [x] Code checks — PASS: `python -m compileall -q app tests` and `git diff --check`.
- [x] Authentication scope — PASS: external authentication is excluded; the
  local development session is explicit and no provider credentials exist.
- Independent QA, commit, and GitHub synchronization remain pending.

## Independent QA handoff

## Engineering correction handoff

- Removed external authentication and Google/OAuth routes, schemas, tests, UI
  wording, environment placeholders, and release references.
- Kept only the explicit `AUTH_DISABLED=1` local session boundary.
- Updated the contract to 17 operations and synchronized GitHub issue bodies.
- Checks: backend 8 tests, frontend 4 tests, browser 3 tests, integration 1
  test, and OpenAPI validation with 17 operations all pass.

## Independent QA handoff

**PASS (2026-09-09):** lifecycle, CSRF, expiry, local ownership boundary,
validation, and conflicts pass. External authentication is outside scope.
The formal QA report is recorded on this issue.

## Goal

Implement the contract with a tested private workspace and temporary state.

## Dependencies

- [#3 — Define the OpenAPI contract for boards and tasks](https://github.com/Tselmeg-C/mini-kanban-2026/issues/3)

## Acceptance criteria

- [ ] backend/ implements openapi.yaml with FastAPI and an explicitly temporary in-memory store. Document local run/test commands and explicit seed setup; never automatically inject development users into real authentication.
- [ ] Implement the local development session, current-session, expiry, and sign-out. Test invalid/expired session behavior; an absent or expired session grants no workspace access.
- [ ] Derive ownership from authenticated identity and enforce it on every board/task operation, search, and direct-ID access. Two-account tests prove foreign data cannot be read, modified, moved, or deleted.
- [ ] Implement board creation/rename/open-recency/archive/restore, fixed columns, title-only To Do task creation, editing, all status transitions, permanent deletion, and title/description search including archived results.
- [ ] Reject invalid fields/statuses and ownership or board reassignment. Preserve creation ordering and distinguish unavailable records without leaking foreign content; archived boards allow all task operations.
- [ ] Atomically reject stale task mutations using the contract's precondition. Tests show a stale save/move cannot overwrite a newer task and a deleted task cannot be recreated through update.
- [ ] Endpoint tests cover documented response schemas/statuses, lifecycle, empty results, validation, session failure, isolation, and conflicts. No external authentication verification is required.

## Out of scope

- External authentication, hosted privacy, SQLite persistence, real frontend
  integration, or hosting. Public identity and account isolation are outside
  this project.
- Those belong to issues #6, #5, and #8 respectively.

## Constraints

- Never print, log, commit, or embed credentials; document configuration names with placeholders.
- Use no password-login fallback or public shared workspace.
- Follow the PM → engineering → independent QA lifecycle; only the orchestrator closes after QA PASS.

## Verification

Run backend and contract checks. Exercise local session sign-in/sign-out,
expiry, CSRF, ownership boundaries, and conflicts. No external credentials are
needed.

## References

- `project-spec.md`
- `instruction.md`
- `AGENTS.md`
- `docs/process.md`
- `docs/team/pm.md`
- `docs/task-template.md`
- Product acceptance criteria: 1, 2, 3, 4, 6, 7, 8, 9, 10, 12.

Source documents are currently available in the local checkout; they have not yet been committed or published to GitHub. Review them there before implementation.
