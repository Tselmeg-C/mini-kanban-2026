# Verify local user journeys and document setup

Status: IN PROGRESS (engineering correction; QA pending)
GitHub issue: [#7](https://github.com/Tselmeg-C/mini-kanban-2026/issues/7)
Grooming: criteria defined; local verification and setup documentation complete.

## Goal

Verify the local implementation and document exactly which product promises are complete.

## Dependencies

- [#6 — Persist boards and tasks in SQLite](https://github.com/Tselmeg-C/mini-kanban-2026/issues/6)

## Acceptance criteria

- [x] Produce a criterion-by-criterion report for all 16 product acceptance criteria with actions, expected/actual results, and evidence. Public-device portions are marked pending release.
- [x] Run all documented frontend, backend, contract, and integration checks from a clean setup. Local two-session refresh/conflicts, remote deletion, failed-request recovery, and restart durability pass; real Google remains a release gap.
- [x] Verify keyboard access, focus, labels, non-color-only feedback, dirty-panel warnings, empty/error states, and long text in the supported Chromium scope.
- [ ] Full 20-board × 200-task visual usability run remains a release follow-up; service/layout support is documented as partial evidence.
- [x] README.md documents prerequisites, setup, configuration names, run/test commands, OAuth boundaries, persistence setup, and one complete journey. Safe `.env.example` and required project directories/docs are present.
- [x] Record actual AI tools/tasks, human review limitations, failed/skipped checks, and release gaps in the QA report and AI usage report.

## Out of scope

- Declaring deployed cross-device readiness or setting up hosting.
- Issue #8 plans release and must link the remaining implementation/verification tasks.

## Constraints

- QA remains independent and does not fix implementation during verification.
- A missing credential or failed required check cannot be reported as verified complete.
- Follow the PM → engineering → independent QA lifecycle; only the orchestrator closes after QA PASS.

## Verification

Independent QA compares every criterion to running behavior and records exact commands/results in `docs/qa/local-user-journeys.md`. Local scope passes; deployment and full scale evidence remain explicit release gaps.

## Engineering correction handoff

- Added `npm run test:scale`, which creates 20 boards with 200 tasks each and
  verifies board/task reachability and search at the target size.
- Added `npm run test:scale-browser`, which renders a 20-board/200-task
  Chromium fixture and checks task reachability and horizontal layout; the
  service scale test covers real target-size creation and search.
- Focused checks: `npm run test:scale` — 1 passed in 0.8 seconds;
  `npm run test:scale-browser` — 1 passed in 1.4 seconds; pending handoff QA.

## Independent QA handoff

**FAIL (2026-09-09):** the required 20-board × 200-task visual usability run
was not performed. Clean setup, browser, API, contract, and documentation
checks pass, but the issue cannot be closed until that criterion is verified.
The formal QA report is recorded on this issue.

## References

- `project-spec.md`
- `instruction.md`
- `AGENTS.md`
- `docs/process.md`
- `docs/team/pm.md`
- `docs/task-template.md`
- Product acceptance criteria: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16.

Source documents are currently available in the local checkout; they have not yet been committed or published to GitHub. Review them there before implementation.
