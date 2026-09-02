# Atlas Pulse Architecture

Atlas Pulse is a modular Django monolith for Industrial IoT. The application
keeps public identity separate from private organization data so users can
belong to multiple organizations while devices, telemetry, alerts and
automations remain isolated.

## System Flow

```text
Machine
  -> Edge Gateway
  -> MQTT / REST
  -> Atlas Pulse
  -> Telemetry Storage
  -> Alerts / Automation / Dashboard
```

## Module Map

- `accounts`: users, authentication, email verification and profile data.
- `organizations`: organizations, memberships, invitations and active context.
- `devices`: device inventory and per-device views.
- `gateways`: edge gateway inventory and connectivity metadata.
- `telemetry`: telemetry data points and ingestion persistence.
- `alerts`: alert rules, alert events and acknowledgement flows.
- `automations`: automation definitions and execution records.
- `integrations`: MQTT and future protocol adapters.
- `api`: REST interface and API permissions.
- `audit`: auditable records for sensitive or autonomous actions.
- `core`: shared services and dashboard pages.

## Tenancy Model

Organization ownership is the primary isolation boundary. Any model containing
industrial data must be scoped to an organization either directly or through a
parent entity that is organization-owned.

Views, serializers, querysets, service functions and background workers must
receive or derive the organization context before reading or writing
organization-owned data.

## Evolution Rules

- Prefer local services inside the monolith before extracting processes.
- Keep cross-module calls explicit and small.
- Introduce new infrastructure only for a measurable bottleneck or reliability
  requirement.
- Treat protocol integrations as adapters that validate external input before
  calling core domain services.

## Future Extension Points

- OPC-UA, Modbus TCP/RTU, LoRaWAN, BACnet and SNMP adapters.
- Edge buffering and offline replay.
- OTA firmware update workflows.
- X.509 certificate-based device identity.
- Time-series storage such as TimescaleDB when telemetry volume requires it.
- Metrics and tracing with Prometheus, Grafana and OpenTelemetry.
