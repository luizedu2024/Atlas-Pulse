from django.conf import settings
from django.db import models


class AutomationRule(models.Model):
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="automation_rules")
    name = models.CharField(max_length=180)
    device = models.ForeignKey("devices.Device", on_delete=models.CASCADE, related_name="automation_rules")
    trigger_type = models.CharField(max_length=60, default="telemetry_threshold")
    metric = models.CharField(max_length=80)
    operator = models.CharField(max_length=3)
    threshold = models.FloatField()
    action_type = models.CharField(max_length=80, default="send_command")
    action_payload = models.JSONField(default=dict, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DeviceCommand(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    device = models.ForeignKey("devices.Device", on_delete=models.CASCADE, related_name="commands")
    command = models.CharField(max_length=120)
    payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    requested_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    response = models.JSONField(default=dict, blank=True)
