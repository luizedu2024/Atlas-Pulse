# Atlas Pulse

Atlas Pulse is an open-source Industrial IoT platform designed to connect devices, machines and edge gateways to the cloud, enabling telemetry, monitoring, alerts, automation and remote management.

## Architecture

```text
Machine
  -> Edge Gateway
  -> MQTT / REST
  -> Atlas Pulse
  -> Telemetry Storage
  -> Alerts / Automation / Dashboard
```

The project is built as a Django multi-tenant application. Public identity is separate from private organizations:

```text
Public Identity + Private Organizations + Isolated Industrial Data
```

Users can register publicly, verify their email, create an organization, accept invitations and switch between organizations. Devices, gateways, telemetry, alerts and automations are always scoped to the active organization.

## Stack

- Django, Django REST Framework, Channels
- PostgreSQL, Redis, Celery, Celery Beat
- Mosquitto MQTT broker
- Django templates, CSS, JavaScript and Chart.js
- django-axes for login brute-force protection
- JWT API authentication via Simple JWT

## Local Setup

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open `http://localhost:8000`.

Demo login:

```text
admin@atlaspulse.local
admin12345
```

## Docker

```bash
docker compose up --build
```

Then run migrations and seed data in another terminal:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_demo
```

## Public Auth Flow

```text
Visitor -> Register -> Verify Email -> Login -> Onboarding -> Create Organization -> Dashboard
```

Invitation flow:

```text
Invite Link -> Register or Login -> Verify Email -> Accept Invitation -> Dashboard
```

Routes:

- `/` public landing page
- `/register/` public registration
- `/login/` login
- `/verify-email/<token>/` email verification
- `/verify-email-required/`
- `/onboarding/`
- `/organizations/create/`
- `/organizations/invite/`
- `/profile/`
- `/password-reset/`

## API

REST API prefix:

```text
/api/v1/
```

JWT:

```text
POST /api/v1/auth/token/
POST /api/v1/auth/token/refresh/
```

Resources:

```text
GET /api/v1/devices/
GET /api/v1/devices/<id>/
GET /api/v1/devices/<id>/telemetry/
POST /api/v1/devices/<id>/commands/
GET /api/v1/gateways/
GET /api/v1/alerts/
GET /api/v1/alert-rules/
```

## MQTT Test

```bash
mosquitto_pub \
  -t atlas/demo/motor-001/telemetry \
  -m '{"metrics":{"temperature":{"value":75,"unit":"C"}}}'
```

Default topic:

```text
atlas/{organization}/{device}/telemetry
```

## Tests

```bash
python -m pytest -q
```

## Future Phase

Documented future extensions include OPC-UA, Modbus TCP/RTU, LoRaWAN, BACnet, SNMP, edge buffering, OTA firmware updates, X.509 certificates, digital twins, Grafana, Prometheus, TimescaleDB and AI anomaly detection.

