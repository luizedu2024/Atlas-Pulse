# Atlas Pulse - Agent Instructions

Atlas Pulse is an open-source Industrial IoT platform built initially as a
modular Django monolith.

## Core Architecture

- Django and Django REST Framework
- PostgreSQL
- Redis and Celery
- MQTT with Mosquitto or EMQX
- React or Next.js for future frontend expansion
- Docker for development
- pytest for tests

## Required Flow

For meaningful product, frontend or backend changes:

1. Delegate requirements analysis to the `analyst` agent.
2. Delegate technical design to the `architect` agent.
3. Delegate frontend design decisions to the `webdesigner` agent when UI, UX,
   templates, dashboards, styling or frontend flows are affected.
4. Delegate backend implementation to the `backend` agent.
5. Delegate tests to the `qa` agent.
6. Delegate final review to the `reviewer` agent.
7. Delegate documentation updates to the `documenter` agent.
8. Wait for all required agents.
9. Consolidate the results in the main agent.

## Rules

- Start as a modular monolith.
- Do not create microservices without a proven bottleneck.
- Never mix data from different organizations.
- Every relevant change must include tests.
- Autonomous AI actions must be auditable.
- Devices and telemetry must never trust the client directly.
- Do not allow multiple agents to edit the same file at the same time.

## Repository Boundaries

- `accounts`: public identity, authentication, registration, profile and email verification.
- `organizations`: organizations, memberships, invitations and active-organization context.
- `devices`: industrial devices and device-level UI.
- `gateways`: edge gateways and gateway metadata.
- `telemetry`: telemetry persistence models.
- `alerts`: alert rules and alert events.
- `automations`: automation rules and executions.
- `integrations`: protocol adapters such as MQTT consumers and parsers.
- `api`: REST serializers, views, permissions and versioned API URLs.
- `audit`: audit trail for security-sensitive and autonomous actions.
- `core`: landing pages, dashboard views and shared domain services.
- `templates`, `static`: server-rendered UI, CSS, JavaScript and frontend assets.

## Security Defaults

- All organization-owned models must be filtered by the active organization.
- API endpoints must enforce authentication and organization membership.
- Device credentials, gateway tokens and integration secrets must not be logged.
- Telemetry ingestion must validate organization, device identity and payload shape.
- Replayed or duplicated ingestion messages should be handled idempotently where possible.

## Testing Expectations

- Use `python -m pytest -q` for the default test suite.
- Add focused tests for new behavior.
- Include cross-organization isolation tests for organization-scoped data.
- Include invalid input and unauthorized access tests for API or ingestion changes.
