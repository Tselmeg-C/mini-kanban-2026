# Define product assumptions and implementation plan

Status: DONE (independent QA PASS)
GitHub issue: [#1](https://github.com/Tselmeg-C/mini-kanban-2026/issues/1)
Grooming: reviewed against the task template; existing criteria retained.
Implementation: planning documents written; independent QA pending.

## Goal

Make the agreed product scope and development phases unambiguous before implementation.

## Dependencies

None.

## Acceptance criteria

- [ ] Review every item under project-spec.md's Assumptions for review and record its disposition. Keep material choices requiring user input explicitly unresolved until reviewed; do not present assumptions as approved.
- [ ] Record concrete validation limits, duplicate-name behavior, creation-time ordering/tie handling, board-recency behavior, search matching/results order, and supported desktop browsers, with a checkable expected result for each.
- [ ] Write an implementation plan outside the product-only spec covering frontend service boundaries, local session handling, ownership, temporary storage then SQLite, automatic refresh, stale-write detection, and draft preservation.
- [ ] Reconcile instruction.md with the later agreed product: project-spec.md is the product document; local development uses SQLite, while public cross-device availability is separately tracked release work. Preserve frontend-first, OpenAPI, tests, and AI reporting deliverables.
- [ ] Map all 16 product acceptance criteria to implementation and verification issues. Identify setup prerequisites by name only, and distinguish local checks from physical cross-device evidence.
- [ ] Document dependencies and phase exit checks. No downstream implementation starts while a material product/security decision needed by it remains unresolved.

## Out of scope

- Application implementation and real cloud setup.
- Local implementation belongs to issues #2–#7; release planning belongs to issue #8.

## Constraints

- Do not expand the approved product scope or choose paid hosting.
- Keep architecture out of project-spec.md; record material new product decisions for user review.
- Follow the PM → engineering → independent QA lifecycle; only the orchestrator closes after QA PASS.

## Verification

Review the decision register and traceability against all product sections. Each disposition and prerequisite must be explicit; planning cannot pass with unacknowledged material blockers.

## References

- `project-spec.md`
- `instruction.md`
- `AGENTS.md`
- `docs/process.md`
- `docs/team/pm.md`
- `docs/task-template.md`
- Product acceptance criteria: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16.

Source documents are currently available in the local checkout; they have not yet been committed or published to GitHub. Review them there before implementation.

## Local engineering handoff

- Plan and decision register: `docs/implementation-plan.md`.
- Reconciled `instruction.md` to use `project-spec.md` and distinguish local SQLite
  delivery from public cross-device release.
- AI assistance and review limits: `docs/ai-usage-report.md`.
- All seven assumption bullets and all 16 product acceptance criteria are covered.
- No application tests apply to this documentation-only change.
- Independent QA, commit/publication, and GitHub handoff remain pending.
  Criteria stay unchecked until independent verification.

## Independent QA handoff

**PASS (2026-09-09):** planning coverage is present, and material release
decisions are explicitly recorded as unresolved or deferred rather than hidden.

## QA: PASS

- [x] Every product-spec assumption has a recorded disposition — PASS.
- [x] Validation limits, duplicate handling, creation ordering/ties, board
  recency, search behavior, and supported browsers have objective checks — PASS.
- [x] The implementation plan covers frontend boundaries, authentication/session
  handling, ownership, storage, refresh, conflicts, and draft preservation — PASS.
- [x] `instruction.md` identifies `project-spec.md` as canonical and preserves
  local SQLite, release boundaries, frontend-first work, OpenAPI, tests, and AI
  reporting — PASS.
- [x] All 16 product criteria are mapped to implementation and verification
  issues with named prerequisites and evidence boundaries — PASS.
- [x] Dependencies and phase exit checks are documented; unresolved release
  decisions are explicitly scoped — PASS.

Tests: planning-document assertion script — 7 assumption rows, 16 criteria
mappings, reconciliation terms, and phase gates present; passed.
Tests: `git diff --check` — passed.
