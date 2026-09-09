# Issue #7 local QA report

Scope: local development on 2026-09-09. The supported browser checks use
headless Chromium available through Playwright. External authentication,
public-device behavior, and release hosting are outside this project.

## Checks

| Check | Command | Result |
| --- | --- | --- |
| Clean frontend install | `cd frontend && npm ci` | PASS; 17 packages, 0 vulnerabilities |
| Backend install and tests | `cd backend && uv sync && uv run python -m unittest discover -s tests -v` | PASS; 7 tests |
| Frontend service tests | `cd frontend && npm test` | PASS; 4 tests |
| Browser mock journey | `cd frontend && npm run test:browser` | PASS; 2 Chromium tests |
| API browser journey | `cd frontend && npm run test:integration` | PASS; disposable SQLite, two sessions, refresh visibility |
| Contract | `cd frontend && npm run validate:openapi` | PASS; 17 operations |

## Product criteria

1. **PASS local scope:** local mock session, two boards, and separate task lists.
   External authentication and hosted privacy are outside `project-spec.md`.
2. **PASS:** board open order and rename behavior are covered by service and API
   lifecycle checks.
3. **PASS:** the UI renders only To Do, In Progress, and Done columns.
4. **PASS:** title-only creation, blank-title validation, and cancel behavior pass.
5. **PASS:** labeled edit panel, explicit save/cancel, dirty-panel confirmation,
   and retained failed-save drafts are implemented and covered.
6. **PASS:** drag and status-selector moves are covered; failed moves retain data.
7. **PASS:** creation timestamps determine stable ordering; no custom ordering API exists.
8. **PASS:** confirmation-gated permanent deletion and Done behavior are covered.
9. **PASS:** archive, restore, archived editing, and archived search are covered.
10. **PASS:** title/description search includes archived boards and empty results.
11. **PASS local scope:** the API browser journey verifies two-session refresh within
    the three-second poll interval.
12. **PASS local scope:** stale version writes conflict without overwriting drafts;
    deleted tasks remain unavailable. Remote-device timing is simulated locally.
13. **PASS local scope:** failed requests retain entered data and expose retryable
    errors; no offline queue is claimed.
14. **PASS:** SQLite restart persistence is covered by backend tests.
15. **PASS local Chromium review:** labels, visible focus outlines, keyboard status
    selection, dialog controls, and `role=status` messages are present. Full
    cross-browser review is a release follow-up.
16. **PARTIAL:** the service and layout support long content and repeated tasks;
    a full 20-board × 200-task visual run is a usability follow-up before hosting.

## Release gaps

- External authentication, real account isolation, and cross-device access are
  outside this project scope.
- Firefox, Edge, Safari, physical-device, network-loss, and full scale visual
  checks are not claimed from this local Chromium run.
