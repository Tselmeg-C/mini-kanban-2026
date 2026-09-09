# TidyBoard cross-device release plan

This is a planning artifact for issue #8. It makes release requirements and
evidence explicit without selecting a provider, provisioning infrastructure, or
claiming production readiness.

## Required release capabilities

- Public HTTPS frontend and API with secure headers, a configured production
  origin, and no credentialed wildcard CORS.
- If a future public release is considered, it needs a separately approved
  authentication design; this project does not define or implement one.
- Durable production storage that preserves owner identity, boards, tasks,
  versions, archive state, and recency across service restarts.
- Backups, restore rehearsal, retention/deletion policy, migration rollback, and
  operational logging that excludes tokens, cookies, and task privacy data.
- Monitoring for availability, authentication failures, database errors, stale
  writes, and failed background refreshes, with an owner and response path.

## Decisions requiring user review

The following remain unresolved and no provider is selected here: hosting
provider and region, monthly budget, production database technology, backup
retention and deletion window, domain/DNS ownership, incident ownership, and
whether the local SQLite data is migrated or treated as development-only.

## Follow-up work

- [#9 Release implementation](9-release-implementation.md): make the selected
  production architecture secure, durable, observable, and recoverable.
- [#10 Deployed verification](10-deployed-verification.md): independently test
  the deployed product on two actual devices and record release evidence.

## Required deployed evidence

Any future deployed QA must use an explicitly approved authentication design on
two actual devices. It must create and edit work, observe updates within about
five seconds, exercise stale conflicts and remote deletion, simulate connection
failure and retry, restart the service, and confirm the same work remains.
Record exact URLs, browser/device versions, elapsed observations,
rollback/restore result, and failed or skipped checks. Local mock sessions and
local SQLite do not substitute for this evidence.

## Rollback boundary

Before release, capture a database backup and migration version. A failed
deployment must be reversible to the previous application and schema version;
restore must be tested against a disposable copy before declaring recovery.
