# Retrospective QA correction record

Performed 2026-09-09 by the single QA engineer to correct the historical record.
QA did not modify implementation, tests, or product scope. This retrospective
record is evidence of the correction only; future work must use one formal
criterion-by-criterion QA report immediately after each engineering handoff.

## Shared evidence

- `cd backend && uv run python -m unittest discover -s tests -v`: 7 passed.
- `cd frontend && npm test`: 4 passed.
- `cd frontend && npm run test:browser`: 2 Chromium tests passed.
- `cd frontend && npm run test:integration`: 1 API integration test passed.
- `cd frontend && npm run validate:openapi`: 18 operations valid.
- Python compile, Node syntax, and `git diff --check`: passed.

## Handoff verdicts

| Issue | Independent verdict | Evidence and remaining work |
| --- | --- | --- |
| #1 planning | PARTIAL | Planning covers all seven assumptions, 16 criteria, prerequisites, boundaries, and gates. Material release decisions remain unresolved and no earlier independent QA record existed. |
| #2 mock frontend | PARTIAL | Current mock lifecycle, validation, drafts, conflicts, archive, search, keyboard-visible controls, and Chromium journey pass. Full long-content/scale and browser-matrix evidence is absent. |
| #3 OpenAPI | PASS | Contract parses, validates, maps service operations, and documents auth, ownership, validation, conflicts, ordering, and errors. |
| #4 API/auth | PASS for approved local scope | Backend lifecycle, CSRF, expiry, ownership boundary, validation, conflicts, and safe unconfigured OAuth behavior pass. Real Google and two external accounts were not tested because authentication was explicitly deferred. |
| #5 API client/refresh | PARTIAL | Real client, mock mode, local two-session refresh, errors, and integration pass. Polling stops when no board is open, so board-list changes there are not refreshed; hosted cross-device evidence is absent. |
| #6 SQLite | PARTIAL | Restart persistence, isolated tests, archive/search, ownership, deletion, and sequential stale writes pass. Genuine concurrent writes are untested and the route check/mutate/persist path has no explicit atomic lock or conditional database update. |
| #7 local QA/setup | FAIL | The required 20-board × 200-task visual usability run was not performed. Other clean setup, browser, API, contract, documentation, and criterion-report checks pass. |

## Process action

Issues #2, #5, #6, and #7 return to engineering/open status. Issue #1
remains open. Issue #3 is independently passed. Issue #4 is independently
passed only under the user-approved local-authentication scope; its release
OAuth gap remains explicit.
