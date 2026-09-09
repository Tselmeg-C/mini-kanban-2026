# Implement the private kanban API and Google sign-in

Status: DONE (independent QA PASS for approved local scope; authentication deferred)
GitHub issue: [#4](https://github.com/Tselmeg-C/mini-kanban-2026/issues/4)
Grooming: criteria defined. The user explicitly deferred authentication from this
project milestone; real Google OAuth, private hosted workspaces, and external
account verification are release follow-up work.

## Local engineering handoff

- `backend/` contains the FastAPI app, temporary in-memory store, lifecycle
  routes, search, and version conflicts. Session/authentication work is deferred.
- `uv run python -m unittest discover -s tests -v` passes 6 endpoint tests.
- `npm run validate:openapi` passes the root contract with 18 operations.
- Real Google sign-in, private account isolation, and two-account verification are
  explicitly deferred and must not be presented as completed.

## QA: PASS for the revised local scope

- [x] FastAPI app and temporary store — PASS: backend test suite passed 6 tests.
- [x] Session expiry, sign-out boundary, CSRF, validation, lifecycle, search,
  and stale-write behavior — PASS: `uv run python -m unittest discover -s tests -v`.
- [x] Ownership behavior within the explicit test-session boundary — PASS: foreign
  board/task reads and search return unavailable/empty results.
- [x] Contract and startup — PASS: `npm run validate:openapi` reports 18 operations;
  `/openapi.json` returned HTTP 200 from Uvicorn.
- [x] Code checks — PASS: `python -m compileall -q app tests` and `git diff --check`.
- [x] Authentication scope — PASS: Google OAuth is explicitly deferred by user
  decision; unconfigured callback behavior is safe and no OAuth completion claim
  is made.
- Independent QA, commit, and GitHub synchronization remain pending.

## Independent QA handoff

**PASS for approved local scope (2026-09-09):** lifecycle, CSRF, expiry,
ownership boundary, validation, conflicts, and safe unconfigured OAuth behavior
pass. Real Google and two external-account checks remain intentionally deferred.
See `docs/qa/independent-handoff-audit.md`.

## Goal

Implement the contract with a tested private workspace and temporary state.

## Dependencies

- [#3 — Define the OpenAPI contract for boards and tasks](https://github.com/Tselmeg-C/mini-kanban-2026/issues/3)

## Acceptance criteria

- [ ] backend/ implements openapi.yaml with FastAPI and an explicitly temporary in-memory store. Document local run/test commands and explicit seed setup; never automatically inject development users into real authentication.
- [ ] Implement Google sign-in, current-session, expiry, and sign-out. Test denied/invalid callback and invalid/expired session behavior; unsuccessful authentication grants no workspace access. Use the security protections required by the selected flow.
- [ ] Derive ownership from authenticated identity and enforce it on every board/task operation, search, and direct-ID access. Two-account tests prove foreign data cannot be read, modified, moved, or deleted.
- [ ] Implement board creation/rename/open-recency/archive/restore, fixed columns, title-only To Do task creation, editing, all status transitions, permanent deletion, and title/description search including archived results.
- [ ] Reject invalid fields/statuses and ownership or board reassignment. Preserve creation ordering and distinguish unavailable records without leaking foreign content; archived boards allow all task operations.
- [ ] Atomically reject stale task mutations using the contract's precondition. Tests show a stale save/move cannot overwrite a newer task and a deleted task cannot be recreated through update.
- [ ] Endpoint tests cover documented response schemas/statuses, lifecycle, empty results, validation, session failure, isolation, and conflicts. Record actual Google sign-in verification separately from simulated automated tests; missing configuration remains an explicit incomplete criterion.

## Out of scope

- Google authentication, private account isolation, SQLite persistence, real
  frontend integration, or hosting. Authentication and privacy belong to a
  future release follow-up.
- Those belong to issues #6, #5, and #8 respectively.

## Constraints

- Never print, log, commit, or embed credentials; document configuration names with placeholders.
- Use no password-login fallback or public shared workspace.
- Follow the PM → engineering → independent QA lifecycle; only the orchestrator closes after QA PASS.

## Verification

Run backend and contract checks. Exercise Google sign-in/sign-out using authorized configuration and two accounts; report external checks blocked by missing credentials honestly.

## References

- `project-spec.md`
- `instruction.md`
- `AGENTS.md`
- `docs/process.md`
- `docs/team/pm.md`
- `docs/task-template.md`
- Product acceptance criteria: 1, 2, 3, 4, 6, 7, 8, 9, 10, 12.

Source documents are currently available in the local checkout; they have not yet been committed or published to GitHub. Review them there before implementation.
