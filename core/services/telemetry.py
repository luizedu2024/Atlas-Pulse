from django.utils import timezone

from devices.models import Device
from telemetry.models import TelemetryPoint
from core.services.alerts import AlertService


class TelemetryRepository:
    @staticmethod
    def latest_for_organization(organization, limit=200):
        return TelemetryPoint.objects.filter(organization=organization).select_related("device")[:limit]

    @staticmethod
    def series_for_device(device, metric, since):
        return TelemetryPoint.objects.filter(device=device, metric=metric, timestamp__gte=since).order_by("timestamp")


class TelemetryService:
    @classmethod
    def ingest_payload(cls, organization, device_id, payload):
        device = Device.objects.select_related("organization").get(organization=organization, device_id=device_id)
        timestamp = payload.get("timestamp") or timezone.now()
        metrics = payload.get("metrics", {})
        points = []
        for metric, reading in metrics.items():
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
        device.status = Device.Status.ONLINE
        device.last_seen = timezone.now()
        device.save(update_fields=["status", "last_seen", "updated_at"])
        return points
