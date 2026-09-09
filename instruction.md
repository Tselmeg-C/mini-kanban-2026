# Build and Ship an AI-Assisted Full-Stack App

Use this instruction to build a small, working end-to-end application with an
AI coding assistant. The application may be a Snake Arena, mini-kanban, or
another similarly small product. Keep the workflow controlled: AI may draft
code, but every phase must be reviewed, run, and tested before the next phase.

## Project-specific scope

`project-spec.md` is the canonical product document. The local milestone uses
SQLite and preserves the frontend-first, OpenAPI, test, and AI-reporting phases
below. Public cross-device availability remains a product requirement; issue #8
plans separately authorized release implementation and deployed verification.
Local browser sessions do not prove physical cross-device acceptance.
See `docs/implementation-plan.md` for decisions, dependencies, and exit checks.

## Non-negotiable repository contract

The repository MUST contain these paths by the end of the work:

```text
project-spec.md             # scope, user stories, acceptance criteria, non-goals
AGENTS.md                   # agent instructions, commands, and project conventions
frontend/                   # maintainable UI and frontend tests
backend/                    # FastAPI application, domain code, and backend tests
openapi.yaml                # reviewed frontend/backend contract
tests/                      # cross-application or shared test helpers
docs/ai-usage-report.md     # AI tools, prompts/tasks, human review, limitations
README.md                   # setup, run, test, and core user journey
```

Additional files and directories are allowed only when they support the
product. Keep generated files, caches, secrets, and local databases out of
version control. Add a `.gitignore` covering at least virtual environments,
frontend dependency directories, build output, `.env` files, test caches, and
SQLite database files.

The finished repository MUST satisfy all of these requirements:

- `project-spec.md` exists before application code is generated.
- The frontend is runnable locally and has a maintainable source structure;
  do not leave an AI prototype as an unreviewed or unstructured export.
- All frontend-to-backend communication goes through one frontend service or
  client layer. Components must not call HTTP endpoints directly.
- `openapi.yaml` is the source of truth for the frontend/backend boundary.
  Every implemented operation has a method, path, parameters, request body,
  success response, error responses, schemas, and authentication requirement
  where applicable.
- `backend/` contains a FastAPI application unless `project-spec.md` records
  a concrete reason to use another backend stack.
- Backend work starts with a mock or in-memory store, then replaces only that
  store with SQLite. API behavior and the frontend service interface must not
  change during the persistence swap.
- SQLite is the required local durable database. Database configuration must be
  environment-driven and the data-access code must avoid PostgreSQL-specific
  behavior so PostgreSQL can replace SQLite later without a domain rewrite.
- The app starts locally from commands documented in `README.md`, persists
  data in SQLite, and serves the core user journey successfully.
- Automated tests cover the key frontend states, key backend endpoints, the
  acceptance criteria in `project-spec.md`, contract behavior, validation, and
  important error cases.
- `docs/ai-usage-report.md` records the AI tools used, major prompts or tasks
  delegated, human review performed, and notable limitations or corrections.
- No secrets, real credentials, `.env` files, or user-specific absolute paths
  are committed. Provide `.env.example` when configuration needs environment
  variables.

Do not add Docker, Docker Compose, deployment, CI/CD, managed PostgreSQL,
WebSocket infrastructure, or production hosting requirements for this module.
Those belong to the deployment module unless the product specification
explicitly requires a small local equivalent.

## Working rules

- Start with user behavior and the product problem, not a database schema.
- Keep the first release small. Record non-goals instead of implementing
  speculative features.
- Prefer the simplest working implementation and existing project patterns.
- Keep frontend, backend, and storage changes separately reviewable.
- Preserve the mock client so frontend-only development and tests remain
  possible after the real API client is added.
- Never weaken validation, authorization, or error handling to make integration
  convenient.
- At the end of every phase, run the app and relevant tests. Fix failures in
  the current phase before continuing.
- Keep commits small and coherent. Update `AGENTS.md` whenever commands,
  conventions, or verification steps become stable.

## Phase 0: Write the product specification

Create `project-spec.md` before generating application code. It MUST define:

- target users and their goals;
- primary user journeys, entry points, and success outcomes;
- screens and visible loading, empty, success, and error states;
- core domain objects and lifecycle rules;
- input validation, authorization, and error behavior;
- non-functional requirements that actually apply;
- testable acceptance criteria;
- explicit non-goals; and
- technical constraints and integration boundaries.

Resolve critical ambiguity before coding. Do not silently invent a requirement
that changes scope or security.

**Exit check:** another developer can implement and review the core behavior
from `project-spec.md` alone.

## Phase 1: Build the frontend against a mock service

1. Build `frontend/` from `project-spec.md`.
2. Define one service/client interface for all data reads and actions.
3. Implement a mock service with representative seed data, loading states,
   empty states, error states, and required mutations.
4. Keep HTTP out of UI components.
5. Add focused frontend tests for the critical journeys and states.
6. Run the frontend locally and manually exercise every acceptance criterion.

**Exit check:** the complete frontend is interactive, tested, and runnable
without backend code.

## Phase 2: Define the OpenAPI contract

Create `openapi.yaml` at the repository root from the frontend service
interface and product specification. For every operation, specify:

- HTTP method and path;
- path, query, and header parameters;
- request body and validation rules;
- successful response status and body;
- expected error statuses and bodies;
- reusable data schemas; and
- authentication and authorization requirements.

Keep the contract implementation-independent. It must describe the product
behavior, not database tables or ORM internals. Review it from both frontend
and backend perspectives before implementation.

**Exit check:** every service operation maps to an OpenAPI operation and every
required user journey has all the API operations it needs.

## Phase 3: Implement the FastAPI backend with temporary state

Create `backend/` to implement `openapi.yaml` exactly. Use FastAPI and a
simple in-memory or mock repository first. Keep these concerns easy to find:

- HTTP routes and serialization;
- domain rules and validation;
- repository/store behavior;
- configuration; and
- authentication/authorization when required by the contract.

Seed useful development data explicitly. Add backend tests for key endpoints,
status codes, request validation, domain rules, authorization, and error
responses. Add a `Makefile` or equivalent with predictable `run` and `test`
commands, plus checks required by the selected stack.

**Exit check:** the backend runs, its tests pass, and its API behavior agrees
with `openapi.yaml`.

## Phase 4: Connect frontend and backend

Add the real frontend client while preserving the existing service interface.
Select the mock or real implementation through a small configuration boundary,
such as an environment variable. Configure local API URLs, CORS, credentials,
and authentication handling as required by the contract.

Run both applications locally and test every acceptance criterion against the
real API, including invalid input, unauthorized behavior, empty results, and
server errors. Fix contract mismatches in `openapi.yaml`, both clients, and
tests together.

**Exit check:** a user can complete every core journey against the real API;
frontend, backend, and integration checks pass with temporary state.

## Phase 5: Replace temporary state with SQLite

Replace only the in-memory repository/store with SQLite. Preserve the OpenAPI
contract, frontend behavior, domain logic, and service interface.

Requirements:

- use migrations or repeatable schema initialization appropriate to the stack;
- configure the database through environment variables with a safe local
  default;
- keep data access portable for a future PostgreSQL deployment;
- seed development data explicitly and never seed it accidentally in
  production; and
- test create/read/update/delete lifecycle behavior, constraints, restart
  persistence, and database errors.

**Exit check:** the complete app runs locally, data survives a backend restart,
and SQLite-backed tests pass.

## Final local release gate

Before declaring the module complete, verify all of the following:

- `project-spec.md`, the frontend service interface, `openapi.yaml`, and the
  implementation describe the same behavior.
- The required repository paths exist and contain maintained, reviewed code.
- The frontend and backend run from documented clean-setup commands.
- Tests pass for the promised acceptance criteria and important failures.
- The app persists data in SQLite and persistence survives restart.
- Required configuration names are documented in `.env.example` without
  secret values.
- Authentication, authorization, validation, and CORS behavior are tested
  where applicable.
- `README.md` explains setup, run commands, test commands, and one complete
  core user journey.
- `docs/ai-usage-report.md` is complete and honest about AI assistance and
  human verification.
- No deployment, container, or CI/CD claim is made unless separately built and
  verified; those are outside this module's required scope.
