# Verify local user journeys and document setup

Status: TODO
GitHub issue: [#7](https://github.com/Tselmeg-C/mini-kanban-2026/issues/7)
Grooming: criteria defined; implementation has not started.

## Goal

Verify the local implementation and document exactly which product promises are complete.

## Dependencies

- [#6 — Persist boards and tasks in SQLite](https://github.com/Tselmeg-C/mini-kanban-2026/issues/6)

## Acceptance criteria

- [ ] Produce a criterion-by-criterion report for all 16 product acceptance criteria with actions, expected/actual results, and evidence. Mark public-device portions pending release rather than claiming a local pass satisfies deployment.
- [ ] Run all documented frontend, backend, contract, and integration checks from a clean setup; exercise real Google access, two-account isolation, two-session refresh/conflicts, remote deletion, offline recovery, and restart durability.
- [ ] Verify keyboard access, focus, labels, non-color-only feedback, dirty-panel warnings, empty/error states, and long text in the supported desktop browser scope decided in issue #1.
- [ ] Verify a workspace with 20 boards and 200 tasks per board: boards/tasks remain reachable, long content does not break layout, search results can be traversed, and loading/saving feedback remains visible. These are usability targets, not hard limits.
- [ ] README.md documents prerequisites, setup, configuration names, run/test commands, Google setup, persistence setup, and one complete journey. Safe .env.example, AGENTS.md, frontend/, backend/, tests/, openapi.yaml, and docs/ai-usage-report.md exist with meaningful content.
- [ ] Record actual AI tools/tasks, human review only when performed, limitations, failed/skipped checks, and release gaps. Sync backlog state; keep each issue open until its independent QA PASS and orchestrator closure.

## Out of scope

- Declaring deployed cross-device readiness or setting up hosting.
- Issue #8 plans release and must link the remaining implementation/verification tasks.

## Constraints

- QA remains independent and does not fix implementation during verification.
- A missing credential or failed required check cannot be reported as verified complete.
- Follow the PM → engineering → independent QA lifecycle; only the orchestrator closes after QA PASS.

## Verification

Independent QA compares every criterion to running behavior and records exact commands/results. Defects go back to engineering; no completion claim from documentation alone.

## References

- `project-spec.md`
- `instruction.md`
- `AGENTS.md`
- `docs/process.md`
- `docs/team/pm.md`
- `docs/task-template.md`
- Product acceptance criteria: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16.

Source documents are currently available in the local checkout; they have not yet been committed or published to GitHub. Review them there before implementation.
