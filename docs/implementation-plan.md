# TidyBoard implementation plan

Issue: [#1](https://github.com/Tselmeg-C/mini-kanban-2026/issues/1)
Status: local planning implementation; independent QA pending.

`../project-spec.md` defines product behavior; `../instruction.md` defines local
delivery. This plan introduces no application code or hosting commitment.
Grooming review: the existing issue contains every task-template section,
checkable criteria, and links for deferred scope; no scope rewrite is needed.

## Decision register

All seven assumption bullets in the product specification are covered below.
Disposition “retained default” means an engineering assumption carried forward
from the existing spec, **not user approval**. None changes the agreed scope or
requires a material new product/security decision before mock UI work.

| Spec assumption | Disposition and concrete rule | Expected check |
| --- | --- | --- |
| Validation | Retained default: trim board names and task titles; require 1–120 Unicode code points after trimming. Description is optional plain text, at most 5,000 code points; omitted means empty. Preserve description whitespace. Reject invalid input without truncation. | Whitespace-only name/title fails; 120 passes and 121 fails; description 5,000 passes and 5,001 fails. Client and server count identically, including emoji. |
| Duplicates | Retained default: duplicate names/titles allowed, records identified by immutable IDs. | Create two identically named boards and tasks; editing one affects only its ID. |
| Task order | Retained default: oldest creation time first in each column; immutable ID ascending breaks equal-time ties. | Equal-time fixtures produce stable order after reload, edit, and movement. |
| Board recency | Retained default: creation/restoration opens the board; explicit opening records server time shared across devices. Both active and archived lists sort last-opened descending, then ID ascending. Polling and renaming do not count as opening. | Open A then B: B comes first in its list; restore A: A opens and becomes first in active boards. Refresh alone never reorders by access time. |
| Search | Retained default: trim query; case-insensitive substring of title or description, including archived boards. Use the same Unicode case-fold comparison in both stores. Empty query shows a prompt. Newest creation time first, ID ascending for ties. Start with the complete matching list and accessible scrolling, with no silent result cap. | Mixed-case and padded queries match; blank query does not list everything; archived matches show labels; every match is reachable. |
| Refresh/conflicts | Retained default: refresh never replaces a draft. Review displays latest content alongside draft; explicit reapplication uses the reviewed version, which can conflict again. | Edit in two sessions: stale save preserves both views; another intervening save causes another conflict. Remote deletion preserves copyable text and disables save. |
| Browsers | Retained default: current stable desktop Chrome, Firefox, Edge, Safari at verification time. Record exact tested versions in #7. Narrow screens retain core access; polished mobile layout and mobile drag are deferred. | Run core keyboard journeys in each browser; narrow-screen content/actions remain reachable using the status selector. Missing browser evidence is pending, never inferred. |

Material release choices remain **unresolved for user review in #8**: public
origin, hosting provider/cost, production storage, backup/retention/recovery, and
production Google OAuth configuration. These block release implementation, not
local mock UI work. Do not start a phase if a newly discovered material product
or security choice needed by that phase is unresolved.

## Implementation boundaries

1. **Frontend first (#2).** Keep UI under `frontend/`. One asynchronous service
   boundary owns session, board list/create/read/rename/open/archive/restore,
   task list/read/create/update/move/delete, and search operations. Components
   call this boundary only. A selectable mock implements all operations and
   reproducible latency, failures, session expiry, conflicts, and remote deletion.
   Keep saved records separate from editable drafts. Select a small frontend
   toolchain during #2; no UI library is required by this plan.
2. **Contract (#3).** Root `openapi.yaml` maps every service operation, including
   Google entry/callback and sign-out, to explicit schemas, validation, statuses,
   errors, and authentication. Record enum wire values and version preconditions
   here before backend coding. Preserve the mock when adding the real client.
3. **Authentication and ownership (#4).** Use FastAPI with an established OIDC
   library for Google's authorization-code flow; validate state, nonce, PKCE,
   issuer, audience, expiry, and registered redirect handling. Identify accounts
   by verified issuer/subject, not user-submitted email or owner IDs. Use opaque,
   server-managed sessions in HttpOnly, SameSite cookies, Secure on HTTPS;
   invalidate on logout and expiry. Permit HTTP only for loopback development.
   Check CSRF tokens and allowed origins for cookie-authenticated mutations;
   restrict credentialed CORS to configured frontend origins. Never put provider
   tokens in browser storage or logs. Session expiry retains drafts without
   exposing one account's draft/data to a different signed-in account.
4. **Temporary then durable store (#4, #6).** Start with a single-process in-memory
   store behind only the operations the routes need. Apply ownership checks to
   all reads and mutations, including search and nested IDs. Missing and foreign
   items return the same unavailable response. Reject owner/board reassignment.
   Replace that store with SQLite and repeatable schema setup in #6, preserving
   routes, service behavior, and contract. Use environment-driven database
   configuration and parameterized portable SQL; avoid PostgreSQL-specific
   behavior. Explicit seeds only. Restart may require sign-in again, but verified
   identity must recover the same durable ownership and content.
5. **Stale writes (#3–#6).** Give each task a version. Require the observed version
   for updates, moves, and deletes; atomically compare and mutate/increment.
   In memory, keep this operation indivisible; in SQLite use a conditional write
   inside a transaction. A mismatched version returns the contract's conflict
   response; a deleted item returns unavailable and never becomes an upsert.
   Conflict review fetches the latest owned record. Do not silently retry a stale
   mutation against a new version.
6. **Refresh and drafts (#5).** Poll relevant board lists, open board/tasks, open
   task, and active search every roughly three seconds while visible/connected;
   refresh immediately on focus/reconnect. Avoid overlapping polls and discard
   obsolete responses after navigation, new search, mutation, or account change.
   Verify observed changes within about five seconds under normal connectivity;
   throttled/background tabs are not guaranteed that timing. Apply fresh saved
   data without replacing draft fields or their base version. Failed saves retain
   input; failed moves show the last confirmed location. Remote deletion retains
   copyable text. Retry is explicit; no offline queue. Warn before discarding dirty
   drafts on navigation/closure. Never claim success before server confirmation.

## Prerequisites and evidence boundaries

Configuration names planned for implementation: `GOOGLE_CLIENT_ID`,
`GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`, `FRONTEND_ORIGIN`, `API_BASE_URL`,
`DATABASE_URL`, and a frontend mock/API mode setting. Final names and safe
placeholders belong in `.env.example` and README when implemented. No credentials
are needed for #1–#3; no secret values are inspected or supplied by this plan.

#4 needs an authorized Google OAuth web client, consent/test-user configuration
where applicable, a registered loopback callback, and two authorized test
accounts. Actual setup or changes to external OAuth settings require user
authorization. Use a reviewed library's required configuration and document
session lifetime before implementation; no long-lived provider access is needed.

Mock identity and mocked OIDC tests prove local behavior only. #4 must separately
record real Google sign-in/out and denied/invalid flows; missing configuration
keeps that criterion incomplete. #5 uses two local browser sessions for timing
and concurrency. #6 uses a disposable SQLite database for restart evidence.
#7 needs access to the four supported desktop browsers. #8 and its future linked
release issues need an authorized public HTTPS environment and two actual
devices; local sessions never substitute for that evidence.

## Product acceptance traceability

Issue numbers refer to the matching files under `docs/backlog/` and GitHub issues.
All rows require final local evidence in #7. Release follow-ups do not exist yet;
#8 must create and link implementation and independent deployed-verification issues.

| Product criterion | Implementation issues | Verification and expected evidence |
| --- | --- | --- |
| 1 Google/private multi-board workspace | #2, #3, #4, #5, #6 | #4 two-account isolation and real Google; #7 local journey; #8 follow-ups actual devices |
| 2 Board recency/rename | #2, #3, #4, #5, #6 | #2 mock order; #4 endpoint checks; #6 persisted recency; #7 journey |
| 3 Fixed columns | #2, #3, #4 | #2 UI; #4 reject invalid statuses; #7 exactly three columns |
| 4 Create/validate/cancel | #2, #3, #4, #5, #6 | #2 drafts/cancel; #4 boundary cases; #6 persistence; #7 title-only creation |
| 5 Side panel/save/cancel/dirty warning | #2, #5, #6 | #2 UI checks; #5 failed-save draft; #7 navigation and persistence |
| 6 Moves/rollback | #2, #3, #4, #5, #6 | #2 drag/selector; #4 all transitions; #5 failed move; #7 keyboard |
| 7 Creation ordering | #2, #3, #4, #6 | #2 and #4 equal-time fixtures/edit/move; #6 reload; #7 no manual reorder |
| 8 Done/delete | #2, #3, #4, #5, #6 | #2 confirmation/cancel; #4 deletion/search; #6 durability; #7 journey |
| 9 Archive/restore/edit | #2, #3, #4, #5, #6 | #2 labels; #4 archived mutations; #6 restart; #7 restore |
| 10 Global search | #2, #3, #4, #5, #6 | #2 navigation/empty; #4 matching/isolation; #7 full result traversal |
| 11 Automatic cross-device updates | #3, #5, #6; #8 release follow-ups | #5 timed local sessions; #7 local report; release QA times actual devices |
| 12 Conflicts/remote deletion | #2, #3, #4, #5, #6 | #4 atomic stale writes; #5 draft/latest/deletion; #6 competing writes; #7 local; release QA devices |
| 13 Connection loss/retry | #2, #5 | #5 offline save/move and reconnect; #7 draft retention; release QA device connection failure |
| 14 Durable same-account access | #4, #6; #8 release follow-ups | #6 service restart/sign-in; #7 browser restart; release QA physical-device access/restart |
| 15 Accessibility | #2, #5 | #2 focused UI checks; #7 keyboard, labels, focus, non-color errors in supported browsers |
| 16 Scale/long content | #2, #5, #6 | #7 20 boards × 200 tasks, long text, feedback and reachable search results |

## Sequential phase gates

| Issue / dependency | Exit evidence before next issue |
| --- | --- |
| #1 / none | Seven assumption dispositions, reconciled instructions, all 16 mapped criteria, explicit prerequisites and unresolved release choices; independent documentation QA PASS and closure. |
| #2 / #1 | Runnable frontend with mock service, reproducible visible/error states, tests and manual keyboard/core journeys; documented commands. |
| #3 / #2 | Validated OpenAPI, complete service-operation mapping, ownership/version/error examples, frontend/backend contract review. |
| #4 / #3 | Running FastAPI with temporary store; endpoint/contract/security checks and separately recorded real Google/two-account evidence. Missing credentials block completion. |
| #5 / #4 | Mock and API clients both usable; full relevant suites, real local journeys, measured two-session refresh, conflicts, deletion, offline retry. |
| #6 / #5 | Same API against SQLite; isolated lifecycle/isolation/concurrency tests; repeatable setup and actual restart persistence. |
| #7 / #6 | Clean-setup checks, all 16 criterion outcomes, browser/scale evidence, README, safe configuration examples, stable AGENTS commands, maintained frontend/backend/tests, OpenAPI and AI report. Public-device portions explicitly pending. |
| #8 / #7 | Reviewed release requirements and outstanding material decisions; actual linked implementation/deployed-QA follow-ups. No provisioning or deployment claim. |

Each issue retains the PM → engineer → independent QA → orchestrator lifecycle
in `process.md`; tests and a running-app check apply once an app exists. Preserve
frontend-first delivery, root OpenAPI, `frontend/`, `backend/`, `tests/`, README,
and `docs/ai-usage-report.md`. No empty application scaffolding is needed in #1.
External changes and pushes require explicit authorization under the global
rules. An engineering self-review does not count as independent QA.
