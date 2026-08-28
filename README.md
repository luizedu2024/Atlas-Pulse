# Atlas Pulse

Atlas Pulse is an open-source Industrial IoT platform designed to connect devices, machines and edge gateways to the cloud, enabling telemetry, monitoring, alerts, automation and remote management.

```text
Machine
  |
Edge
  |
MQTT
  |
Atlas Pulse
  |
Telemetry
  |
Alerts / Automation / Dashboard
```

## MVP

- Login, logout and password reset views
- Custom user model with organization and role
- Multi-tenant organizations
- Devices, gateways, telemetry, alerts, automations, dashboards and audit models
- Django templates dashboard with Chart.js telemetry
- REST API under `/api/v1/`
- MQTT ingestion skeleton using `paho-mqtt`
- Docker Compose with PostgreSQL, Redis, Mosquitto, Celery and Celery Beat
- Demo seed command

## Installation

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open `http://localhost:8000`.

Demo credentials:

```text
username: admin
password: admin123
```

## Docker

```bash
docker compose up --build
```

The web app is available at `http://localhost:8000`. Anonymous users are redirected to `/login/`; authenticated users land on `/dashboard/`.

## MQTT Test

```bash
mosquitto_pub \
  -h localhost \
  -t atlas/demo/motor-001/telemetry \
  -m '{
    "metrics": {
      "temperature": {
        "value": 75,
        "unit": "C"
      }
    }
  }'
```

Run the consumer with:

```bash
python manage.py mqtt_consumer
```

## REST API

Examples:

```text
GET  /api/v1/devices/
GET  /api/v1/devices/<id>/
GET  /api/v1/devices/<id>/telemetry/
GET  /api/v1/gateways/
GET  /api/v1/alerts/
POST /api/v1/devices/<id>/commands/
```

Authentication currently supports Django sessions and DRF tokens. The architecture leaves room for JWT, API keys, device tokens and X.509 certificates.

## Second Phase

Documented but not implemented yet: OPC-UA, Modbus TCP, Modbus RTU, LoRaWAN, BACnet, SNMP, edge buffering, OTA firmware updates, device provisioning, X.509 certificates, digital twins, geolocation maps, Grafana, Prometheus, TimescaleDB, AWS IoT Core, Azure IoT, GCP IoT integrations, AI anomaly detection and predictive maintenance.

