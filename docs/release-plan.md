# TidyBoard cross-device release plan

This is a planning artifact for issue #8. It makes release requirements and
evidence explicit without selecting a provider, provisioning infrastructure, or
claiming production readiness.

## Required release capabilities

- Public HTTPS frontend and API with secure headers, a configured production
  origin, and no credentialed wildcard CORS.
- Google OAuth authorization-code flow with registered HTTPS redirect URI,
  state/nonce/PKCE validation, issuer/audience/expiry checks, secure session
  cookies, logout/expiry invalidation, and CSRF protection for mutations.
- Durable production storage that preserves owner identity, boards, tasks,
  versions, archive state, and recency across service restarts.
- Backups, restore rehearsal, retention/deletion policy, migration rollback, and
  operational logging that excludes tokens, cookies, and task privacy data.
- Monitoring for availability, authentication failures, database errors, stale
  writes, and failed background refreshes, with an owner and response path.

## Decisions requiring user review

The following remain unresolved and no provider is selected here: hosting
provider and region, monthly budget, production database technology, backup
retention and deletion window, domain/DNS ownership, Google consent-screen and
test-user settings, incident ownership, and whether the local SQLite data is
migrated or treated as development-only. Credentials and OAuth changes require
explicit authorization.

## Follow-up work

- [#9 Release implementation](9-release-implementation.md): make the selected
  production architecture secure, durable, observable, and recoverable.
- [#10 Deployed verification](10-deployed-verification.md): independently test
  the deployed product on two actual devices and record release evidence.

## Required deployed evidence

QA must use the same Google account on two actual devices, create and edit work,
observe updates within about five seconds, verify a second account cannot access
it, exercise stale conflicts and remote deletion, simulate connection failure
and retry, restart the service, and confirm the same work remains. Record exact
URLs, browser/device versions, elapsed observations, rollback/restore result,
and any failed or skipped checks. Local mock sessions and local SQLite do not
substitute for this evidence.

## Rollback boundary

Before release, capture a database backup and migration version. A failed
deployment must be reversible to the previous application and schema version;
restore must be tested against a disposable copy before declaring recovery.
