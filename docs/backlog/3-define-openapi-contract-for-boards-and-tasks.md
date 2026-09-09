# Define the OpenAPI contract for boards and tasks

Status: DONE locally (QA PASS; GitHub synchronization pending)
GitHub issue: [#3](https://github.com/Tselmeg-C/mini-kanban-2026/issues/3)
Grooming: criteria defined. Contract implementation is complete locally.

## Local engineering handoff

- Root `openapi.yaml` defines authentication, board, task, status, and search operations.
- `docs/openapi-service-mapping.md` maps every mock service method to an operation.
- `npm run validate:openapi` passes with 18 operations.
- Storage, backend, credentials, and deployment remain out of scope.
- Independent QA PASS: validator and contract assertions passed on 2026-09-09.
- Commit and GitHub synchronization remain pending.

## QA: PASS

- [x] Root OpenAPI parses and validates — PASS: `npm run validate:openapi` reports 18 operations.
- [x] Operation coverage and mapping — PASS: all 18 expected service operations match `docs/openapi-service-mapping.md`.
- [x] Security and ownership boundaries — PASS: protected operations require the session cookie; unavailable responses cover missing and foreign resources.
- [x] Validation, statuses, ordering, search, and conflicts — PASS: schemas and descriptions include the fixed status enum, field limits, ordering, archived metadata, version preconditions, and `409` latest-content responses.
- [x] Contract quality checks — PASS: `git diff --check`.

## Goal

Specify the contract for every frontend service operation before building the backend.

## Dependencies

- [#2 — Build the kanban interface with mock data](https://github.com/Tselmeg-C/mini-kanban-2026/issues/2)

## Acceptance criteria

- [ ] Create valid root openapi.yaml covering Google entry/callback and current-session/sign-out behavior, board list/create/read/rename/open-recency/archive/restore, task list/read/create/update/status/delete, and global task search.
- [ ] Each operation defines method/path, inputs, required/optional fields, validation, success status/body, expected error status/body, and authentication. Define task IDs, statuses, creation ordering, archive labels, and search result metadata.
- [ ] Specify ownership enforcement and non-disclosing behavior for foreign or missing resources. Clients cannot transfer ownership or move tasks across boards. Archived-board operations remain permitted.
- [ ] Specify version/precondition behavior for stale edits and moves, the conflict response and latest-content retrieval, and deletion handling so a stale draft cannot resurrect a deleted task.
- [ ] Document how connected clients refresh board/task/search changes within about five seconds, including deletion detection and ordering. Specify empty search and result traversal consistent with the planning decisions.
- [ ] Map every mock service operation to the contract and validate OpenAPI using a documented runnable check. Include examples for success, invalid input, unauthenticated/foreign access, missing task, and stale write.

## Out of scope

- Backend implementation, credentials, or deployment.
- Frontend draft/conflict UI integration belongs to issue #5.

## Constraints

- Remain storage-independent; no database tables as the public contract.
- Follow issue #1 decisions without silently adding endpoints for excluded features.
- Follow the PM → engineering → independent QA lifecycle; only the orchestrator closes after QA PASS.

## Verification

Run contract validation and review the operation-to-service mapping and error examples. Record validation command and result.

## References

- `project-spec.md`
- `instruction.md`
- `AGENTS.md`
- `docs/process.md`
- `docs/team/pm.md`
- `docs/task-template.md`
- Product acceptance criteria: 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14.

Source documents are currently available in the local checkout; they have not yet been committed or published to GitHub. Review them there before implementation.
