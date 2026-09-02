# Product Requirements

Atlas Pulse helps industrial teams connect machines, gateways and cloud
workflows in one open-source platform.

## Primary Users

- Organization owners who configure teams, devices and integrations.
- Operators who monitor devices, telemetry and alerts.
- Engineers who integrate machines, gateways and industrial protocols.
- Administrators who audit access and automation behavior.

## Core Capabilities

- Public registration, email verification and login.
- Organization creation, invitations and membership management.
- Active organization switching.
- Device and gateway inventory.
- Telemetry ingestion through MQTT and REST.
- Device telemetry history and dashboards.
- Alert rules and alert event tracking.
- Automation rules with auditable executions.
- REST API secured by authentication and organization permissions.

## Acceptance Principles

- A user can only see and operate within organizations they belong to.
- Industrial data is always scoped to an organization.
- Operators can quickly identify device status and recent telemetry.
- Ingestion paths reject malformed or unauthorized telemetry.
- Alerting and automation behavior leaves an auditable trail.

## Near-Term Priorities

- Harden device registration and credential handling.
- Improve telemetry idempotency and payload validation.
- Expand dashboard filtering and status summaries.
- Add richer alert acknowledgement and resolution workflows.
- Document edge gateway setup for local development and production.
