# Plan cross-device release and hosting

Status: IN PROGRESS (engineering handoff; QA pending)
GitHub issue: [#8](https://github.com/Tselmeg-C/mini-kanban-2026/issues/8)
Grooming: criteria defined; implementation has not started.

## Goal

Produce a concrete, reviewable plan for the release required by the cross-device product.

## Dependencies

- [#7 — Verify local user journeys and document setup](https://github.com/Tselmeg-C/mini-kanban-2026/issues/7)

## Acceptance criteria

- [ ] Document deployment requirements for public secure access, Google sign-in redirect configuration, private sessions, persistent storage, and recovery, distinguishing requirements from unapproved provider choices.
- [ ] Identify material hosting, cost, credential, and data-lifecycle decisions for user review. Do not provision infrastructure, change external OAuth settings, or select paid services by assumption.
- [ ] Create and link concrete GitHub follow-up issues for release implementation and independent deployed verification. Each has goal, checkable criteria, exclusions, constraints, dependencies, and a synchronized local backlog file.
- [ ] Follow-up criteria cover the same Google account accessing saved work on two actual devices, updates within about five seconds under normal connectivity, cross-account isolation, conflict/draft behavior, connection failure, and persistence across service restarts.
- [ ] Assign every remaining deployed requirement from the local verification report to a follow-up issue, and document deployment/setup/rollback evidence needed for a release decision.
- [ ] Update todo.md to identify the next unblocked follow-up. Closing this planning issue must not mark deployment or cross-device product acceptance complete.

## Out of scope

- Performing deployment, provisioning paid infrastructure, or claiming production readiness.
- Execution and deployed QA must remain explicit linked follow-up issues created by this planning work.

## Constraints

- Preserve product scope and require user review for material new decisions.
- Keep the local SQLite milestone separate from production storage decisions.
- Follow the PM → engineering → independent QA lifecycle; only the orchestrator closes after QA PASS.

## Engineering handoff

- Added `docs/release-plan.md` with requirements, unresolved user decisions,
  deployed evidence, and rollback boundaries.
- Created linked follow-ups #9 (release implementation) and #10 (deployed
  verification), each with checkable criteria and synchronized local files.
- No infrastructure, OAuth settings, paid provider, or credentials were changed.

## Verification

Review the release plan and actual linked follow-up issues against local gaps and the product's cross-device criteria; check each material choice is resolved or explicitly pending.

## Engineering correction handoff

- Assigned the remaining Firefox, Edge, Safari, physical-device, network-loss,
  and 20-board × 200-task gaps to #10's deployed verification criteria.
- Updated `todo.md` to point to #9 as the next unblocked implementation follow-up
  after this planning issue passes QA.

## References

- `project-spec.md`
- `instruction.md`
- `AGENTS.md`
- `docs/process.md`
- `docs/team/pm.md`
- `docs/task-template.md`
- Product acceptance criteria: 1, 11, 12, 13, 14.

Source documents are currently available in the local checkout; they have not yet been committed or published to GitHub. Review them there before implementation.
