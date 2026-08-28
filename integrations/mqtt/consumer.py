from organizations.models import Organization
from core.services.telemetry import TelemetryService
from .parser import parse_payload, parse_topic


def handle_telemetry_message(topic, payload):
    organization_slug, device_id = parse_topic(topic)
    organization = Organization.objects.get(slug=organization_slug, is_active=True)
    return TelemetryService.ingest_payload(organization, device_id, parse_payload(payload))
