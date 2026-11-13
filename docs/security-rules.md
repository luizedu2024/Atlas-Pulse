# Security Rules

Atlas Pulse handles industrial telemetry, device control and organization data.
Security decisions must favor isolation, auditability and explicit trust
boundaries.

## Organization Isolation

- Never return organization-owned records without filtering by the active
  organization.
- Never infer authorization from a user-supplied organization or object ID alone.
- Check membership before creating, reading, updating or deleting
  organization-owned data.
- Include tests proving a user from one organization cannot access another
  organization's devices, gateways, telemetry, alerts or automations.

## Device And Telemetry Trust

- Devices and gateways are external actors and must not be trusted by default.
- Validate topic structure, organization identity, device identity and payload
  shape before persisting telemetry.
- Do not accept device commands unless the requesting user is authenticated,
  authorized and scoped to the device organization.
- Avoid logging raw credentials, tokens or device secrets.

## Auditability

- Record security-sensitive actions in `audit` where practical.
- Autonomous AI or automation actions must include actor, organization, target,
  action, timestamp and enough metadata to explain what happened.
- Audit logs should be append-only at the application level.

## Authentication

- Keep login brute-force protection enabled.
- Keep password reset and email verification flows generic enough to avoid user
  enumeration.
- Prefer short-lived access tokens and refresh-token rotation for API clients
  when supported.

## Secrets

- Load secrets from environment variables.
- Keep `.env` files out of source control.
- Do not commit broker credentials, JWT secrets, database passwords or API keys.
