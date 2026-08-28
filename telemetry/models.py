from django.db import models


class TelemetryPoint(models.Model):
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="telemetry_points")
    device = models.ForeignKey("devices.Device", on_delete=models.CASCADE, related_name="telemetry_points")
    metric = models.CharField(max_length=80, db_index=True)
    value = models.FloatField()
    unit = models.CharField(max_length=32, blank=True)
    timestamp = models.DateTimeField(db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["organization", "device", "metric", "-timestamp"]),
            models.Index(fields=["organization", "metric", "-timestamp"]),
        ]

    def __str__(self):
        return f"{self.device} {self.metric}={self.value}{self.unit}"
