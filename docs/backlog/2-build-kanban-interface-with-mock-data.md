# Build the kanban interface with mock data

Status: IN PROGRESS (independent QA PARTIAL; reopened)
GitHub issue: [#2](https://github.com/Tselmeg-C/mini-kanban-2026/issues/2)
Grooming: criteria defined. Frontend implementation is now in progress.

## Local engineering handoff

- `frontend/` contains the native HTML/CSS/JavaScript application and mock service.
- `README.md` documents the local run and test commands.
- `npm test` passes the service lifecycle and stale-write checks.
- `node --check app.js` and `node --check service.js` pass; `git diff --check` passes.
- Browser/manual verification remains pending. The sandbox rejected
  `python3 -m http.server 4173` with a port permission error, so the runnable
  browser check is incomplete until run outside this sandbox.
- Independent QA, commit, and GitHub synchronization remain pending.

## Engineering verification (not QA)

- [x] Mock service lifecycle, validation, search, archive, deletion, stale-write,
  and retry behavior — PASS: `npm test` (3 tests passed).
- [x] JavaScript syntax and whitespace checks — PASS: `node --check` and
  `git diff --check`.
- [x] Documented static server — PASS: `python3 -m http.server 4173` served `/`
  with HTTP 200 when run with the required local permission.
- [x] Browser interaction coverage — PASS: `npm run test:browser` passed in
  Chromium for sign-in, board opening, task creation/edit/search/status change,
  dirty-draft cancel, deletion confirmation, archive, and restore.

QA passed on 2026-09-09. Broader browser matrix, scale, and full journey evidence
remain part of issue #7; this local issue is ready for the next dependency.

## Engineering correction handoff

- Added a Chromium check for keyboard task opening, status movement, 120-character
  titles, 5,000-character descriptions, and horizontal overflow.
- Fixed task-card title wrapping with `.task-open strong { overflow-wrap: anywhere; }`.
- Focused check: `npm run test:browser` — 3 passed.

## Independent QA handoff

**PARTIAL (2026-09-09):** current mock lifecycle and Chromium journey pass, but
full long-content/scale and browser-matrix evidence is missing. The formal QA
report is recorded on this issue.

## Goal

Make the complete product workflow usable and testable without a backend.

## Dependencies

- [#1 — Define product assumptions and implementation plan](https://github.com/Tselmeg-C/mini-kanban-2026/issues/1)

## Acceptance criteria

- [ ] frontend/ runs through documented commands without a backend. All data/actions go through one selectable service interface with representative mock data; components make no direct HTTP calls.
- [ ] Show a simulated Google entry/session flow, empty workspace, multiple named boards, recently opened ordering, rename, separate active/archive views, and archive/restore. Archived boards retain their label and all task actions remain usable.
- [ ] Every board has exactly To Do, In Progress, Done. Title-only creation starts in To Do; description is optional. Validate the planning issue's field rules and reject blank titles without losing input.
- [ ] Task selection opens a side panel with title, description, status, Save, Cancel, Delete. Save commits, Cancel discards, and leaving a dirty panel requires a discard decision; failed saves preserve the draft.
- [ ] Support immediate drag-to-column moves and status changes committed by Save, including moves out of Done. Failed moves restore confirmed state; task order stays creation-based and within-column dragging does not reorder.
- [ ] Delete requires permanent-deletion confirmation, cancellation changes nothing, and successful deletion removes search results. Search title/description across all owned mock boards including archives; show board/status/archive label and open the chosen task.
- [ ] Provide reproducible loading, empty, saving, success, validation, unavailable-item, expired-session, network-failure, stale-edit, and remote-deletion states. Refresh must preserve drafts; conflict review shows draft/latest content without blind overwrite.
- [ ] Automated frontend checks cover create/edit/cancel/move/delete, archive editing, search, and draft failures. Verify keyboard navigation, labels, visible focus, non-color-only status/errors, and a desktop layout with long text.

## Out of scope

- Real Google authentication, real API calls, and durable storage.
- Real cross-session refresh is issue #5; full scale/browser verification is issue #7.

## Constraints

- Mock sign-in is clearly development-only and makes no security claim.
- Do not add custom columns, manual task ordering, or unapproved product features.
- Follow the PM → engineering → independent QA lifecycle; only the orchestrator closes after QA PASS.

## Verification

Run frontend tests and manually exercise the mock journey and keyboard status selector. Record exact commands and observed failure/conflict states.

## References

- `project-spec.md`
- `instruction.md`
- `AGENTS.md`
- `docs/process.md`
- `docs/team/pm.md`
- `docs/task-template.md`
- Product acceptance criteria: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16.

Source documents are currently available in the local checkout; they have not yet been committed or published to GitHub. Review them there before implementation.
