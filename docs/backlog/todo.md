# Backlog

GitHub Issues are canonical; these files mirror their current scope and status.
Statuses: TODO = not started; IN PROGRESS = active; DONE = independent QA PASS and orchestrator closure.

PM grooming is complete. #1 has a local planning implementation awaiting independent QA
and GitHub synchronization; all issues remain open.
**NEXT: #5 — Connect the kanban interface to the API and refresh changes.**

- [ ] IN PROGRESS (local; GitHub sync pending) — [#1 Define product assumptions and implementation plan](1-define-product-assumptions-and-implementation-plan.md) · [GitHub](https://github.com/Tselmeg-C/mini-kanban-2026/issues/1)
- [x] DONE locally (QA PASS; GitHub sync pending) — [#2 Build the kanban interface with mock data](2-build-kanban-interface-with-mock-data.md) · [GitHub](https://github.com/Tselmeg-C/mini-kanban-2026/issues/2) · depends on #1
- [x] DONE locally (QA PASS; GitHub sync pending) — [#3 Define the OpenAPI contract for boards and tasks](3-define-openapi-contract-for-boards-and-tasks.md) · [GitHub](https://github.com/Tselmeg-C/mini-kanban-2026/issues/3) · depends on #2
- [x] DONE locally (QA PASS; authentication deferred; GitHub sync pending) — [#4 Implement the private kanban API and Google sign-in](4-implement-private-kanban-api-and-google-sign-in.md) · [GitHub](https://github.com/Tselmeg-C/mini-kanban-2026/issues/4) · depends on #3
- [ ] TODO — [#5 Connect the kanban interface to the API and refresh changes](5-connect-kanban-interface-to-api-and-refresh-changes.md) · [GitHub](https://github.com/Tselmeg-C/mini-kanban-2026/issues/5) · depends on #4
- [ ] TODO — [#6 Persist boards and tasks in SQLite](6-persist-boards-and-tasks-in-sqlite.md) · [GitHub](https://github.com/Tselmeg-C/mini-kanban-2026/issues/6) · depends on #5
- [ ] TODO — [#7 Verify local user journeys and document setup](7-verify-local-user-journeys-and-document-setup.md) · [GitHub](https://github.com/Tselmeg-C/mini-kanban-2026/issues/7) · depends on #6
- [ ] TODO — [#8 Plan cross-device release and hosting](8-plan-cross-device-release-and-hosting.md) · [GitHub](https://github.com/Tselmeg-C/mini-kanban-2026/issues/8) · depends on #7

Keep issue titles, acceptance criteria, status, and dependencies synchronized after each handoff. No application implementation or QA completion is claimed. Source documents are still local and uncommitted.

Cross-device release is outstanding. #8 must create linked implementation and deployed-verification follow-ups; its completion alone does not complete the product.
