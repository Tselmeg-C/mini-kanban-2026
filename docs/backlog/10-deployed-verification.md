# Deployed verification

Status: TODO
GitHub issue: [#10](https://github.com/Tselmeg-C/mini-kanban-2026/issues/10)

## Goal

Independently verify the approved production deployment against the complete
cross-device product behavior.

## Dependencies

- [#9 — Release implementation](9-release-implementation.md)

## Acceptance criteria

- [ ] The same Google account accesses saved work on two actual devices and service restart preserves it.
- [ ] Confirmed board/task changes appear on the second device within about five seconds under normal connectivity.
- [ ] A second account cannot read, search, or mutate the first account's work.
- [ ] Stale edits, remote deletion, connection failure, retry, and draft preservation behave as specified.
- [ ] Current desktop Chrome, Firefox, Edge, and Safari are checked, and the
  20-board × 200-task workspace remains reachable with long content and search.
- [ ] Browser/device versions, URLs, elapsed timings, backup/restore result, failures, and skipped checks are recorded with one overall QA PASS/FAIL.

## Out of scope

- Implementing fixes or changing production configuration during QA.
- Declaring release readiness when any criterion is incomplete.

## Constraints

- Use real deployed HTTPS and authorized test accounts without exposing credentials.
- QA does not modify implementation; failures return to #9.

## Verification

Follow `docs/release-plan.md` and record reproducible deployed evidence for every
criterion.

## References

- `docs/release-plan.md`
- `project-spec.md`
- `docs/process.md`
