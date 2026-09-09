# Development Process

GitHub Issues are canonical. `docs/backlog/<number>-<slug>.md` mirrors each
issue, and `docs/backlog/todo.md` identifies the next unblocked item. Process
one issue at a time in dependency order. Engineering checks are handoff
evidence; they are never called QA.

## Phase 5: Groom one task

The product manager reads the task and linked product documents, rewrites the
standard sections, resolves only supported ambiguity, makes every criterion
independently checkable, links excluded follow-ups, and writes no code. Ask the
user when a missing product decision could materially change behavior.

Grooming is complete only when the goal, dependencies, acceptance criteria,
out-of-scope items, constraints, verification, and references are complete and
a new implementer can work from the issue alone.

## Phase 6: Implement one groomed task

The software engineer reads the complete task, inspects code/tests, implements
only the groomed scope, adds meaningful edge-case tests, runs focused and full
checks, records changes/evidence/concerns, commits, pushes when authorized, and
leaves the issue open. The engineer may report checks, but must not label them
QA or close the issue.

## Phase 7: Verify independently

Use exactly one QA engineer after each engineering handoff. QA reads every
criterion, checks running behavior and code, runs required commands, exercises
important uncovered cases, changes no implementation or tests, and writes one
report per issue in this shape:

```markdown
## QA: PASS | FAIL

- [x] Criterion — PASS
- [ ] Criterion — FAIL: action taken, expected result, actual result, and evidence

Tests: `<command>` — <result>
```

`PASS` is allowed only when every criterion passes. A retrospective aggregate
audit is not a replacement for the per-handoff report.

## Phase 8: Correction loop

`FAIL` returns the exact QA evidence to engineering. Engineering fixes the
defects and leaves the issue open; the same single QA engineer starts a new
verification pass. `PASS` allows the orchestrator to close the issue.

## Phase 9: Backlog loop

The orchestrator selects the next open item, runs grooming, sends it to
engineering, sends that handoff to the one QA engineer, routes failures back to
engineering, and closes only after QA `PASS`. Stop when no open items remain or
when a genuine blocker requires user input.
