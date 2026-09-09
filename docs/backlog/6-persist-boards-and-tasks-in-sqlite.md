# Persist boards and tasks in SQLite

Status: TODO
GitHub issue: [#6](https://github.com/Tselmeg-C/mini-kanban-2026/issues/6)
Grooming: criteria defined; implementation has not started.

## Goal

Make user work durable without changing frontend or API behavior.

## Dependencies

- [#5 — Connect the kanban interface to the API and refresh changes](https://github.com/Tselmeg-C/mini-kanban-2026/issues/5)

## Acceptance criteria

- [ ] Replace the temporary store with SQLite while preserving the OpenAPI contract and frontend service behavior. Persist user ownership, boards/recency/archive state, tasks/status/creation order, and mutation versions.
- [ ] Provide environment-driven database configuration with a safe local default and repeatable schema setup or migrations. Rerunning setup preserves existing data; seed data is explicit.
- [ ] Create boards/tasks, edit/move/archive them, restart the backend with the same database, sign in again, and verify all saved fields, ownership, search results, and archive state remain.
- [ ] Run the existing lifecycle/contract/isolation tests against isolated SQLite data, including invalid input, missing tasks, archived-board edits, and two-account access attempts.
- [ ] Test competing writes so only the matching version succeeds; stale mutation is rejected atomically. A failed write leaves confirmed data intact and deleted tasks are not resurrected.
- [ ] Keep local database files and test artifacts untracked. Document storage setup and portability boundaries; switching to future production storage must not require a product/domain redesign.

## Out of scope

- Production database provisioning or deployment.
- Public durable storage decisions belong to issue #8 and its release follow-ups.

## Constraints

- Tests must not use a developer's shared database.
- Do not sacrifice ownership, conflict checks, or existing behavior for the storage replacement.
- Follow the PM → engineering → independent QA lifecycle; only the orchestrator closes after QA PASS.

## Verification

Run SQLite-backed tests and a real restart-persistence check with a disposable database; record setup repeatability and concurrency results.

## References

- `project-spec.md`
- `instruction.md`
- `AGENTS.md`
- `docs/process.md`
- `docs/team/pm.md`
- `docs/task-template.md`
- Product acceptance criteria: 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 14.

Source documents are currently available in the local checkout; they have not yet been committed or published to GitHub. Review them there before implementation.
