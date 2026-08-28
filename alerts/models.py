from django.conf import settings
from django.db import models


class AlertRule(models.Model):
    class Operator(models.TextChoices):
        GT = ">", ">"
        GTE = ">=", ">="
        LT = "<", "<"
        LTE = "<=", "<="
        EQ = "==", "=="
        NE = "!=", "!="

    class Severity(models.TextChoices):
        INFO = "info", "Info"
        WARNING = "warning", "Warning"
        CRITICAL = "critical", "Critical"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="alert_rules")
    name = models.CharField(max_length=180)
    device = models.ForeignKey("devices.Device", null=True, blank=True, on_delete=models.CASCADE, related_name="alert_rules")
    metric = models.CharField(max_length=80, db_index=True)
    operator = models.CharField(max_length=3, choices=Operator.choices)
    threshold = models.FloatField()
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.WARNING, db_index=True)
    enabled = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["organization", "metric", "enabled"])]

    def __str__(self):
        return self.name


class AlertEvent(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ACKNOWLEDGED = "acknowledged", "Acknowledged"
        RESOLVED = "resolved", "Resolved"

    alert_rule = models.ForeignKey(AlertRule, on_delete=models.CASCADE, related_name="events")
    device = models.ForeignKey("devices.Device", on_delete=models.CASCADE, related_name="alert_events")
    metric = models.CharField(max_length=80, db_index=True)
    value = models.FloatField()
    severity = models.CharField(max_length=20, choices=AlertRule.Severity.choices, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    message = models.TextField()
    triggered_at = models.DateTimeField(auto_now_add=True, db_index=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-triggered_at"]
        indexes = [models.Index(fields=["device", "status", "-triggered_at"])]
