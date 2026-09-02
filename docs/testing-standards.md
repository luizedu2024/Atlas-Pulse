# Testing Standards

Atlas Pulse uses pytest for regression coverage. Tests should focus on behavior,
authorization and isolation rather than implementation details.

## Default Command

```bash
python -m pytest -q
```

## Required Coverage For Relevant Changes

- Happy path for the new behavior.
- Invalid input handling.
- Unauthenticated and unauthorized access, when the behavior is user-facing.
- Cross-organization isolation for organization-scoped data.
- Idempotency or duplicate handling for telemetry ingestion and background jobs.
- Regression tests for bugs fixed.

## Test Data

- Prefer explicit factories or small local setup blocks.
- Use clear organization, user and device names that reveal the authorization
  scenario.
- Avoid relying on global seed data in automated tests.

## External Systems

- Do not require a live MQTT broker, Redis server or external service for unit
  tests.
- Mock protocol clients at module boundaries.
- Keep integration tests clearly marked if they require external dependencies.

## Assertions

- Assert both the response and the persisted data when a behavior writes state.
- For isolation tests, assert that forbidden records are not visible and are not
  mutated.
- For audit-related behavior, assert that the audit entry contains actor,
  organization, action and target context.
