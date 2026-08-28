from django.utils import timezone

from core.services.alerts import AlertService
from devices.models import Device
from telemetry.models import TelemetryPoint


class TelemetryRepository:
    @staticmethod
    def latest_for_organization(organization, limit=200):
        return TelemetryPoint.objects.filter(organization=organization).select_related("device")[:limit]


class TelemetryService:
    @classmethod
    def ingest_payload(cls, organization, device_id, payload):
        device = Device.objects.get(organization=organization, device_id=device_id)
        timestamp = payload.get("timestamp") or timezone.now()
        points = []
        for metric, reading in payload.get("metrics", {}).items():
            point = TelemetryPoint.objects.create(
                organization=organization,
                device=device,
                metric=metric,
                value=float(reading["value"]),
                unit=reading.get("unit", ""),
                timestamp=timestamp,
                metadata=reading.get("metadata", {}),
            )
            AlertService.evaluate_point(point)
            points.append(point)
        device.status = "online"
        device.last_seen = timezone.now()
        device.save(update_fields=["status", "last_seen", "updated_at"])
        return points
