from django.db import models


class Gateway(models.Model):
    class Status(models.TextChoices):
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"
        WARNING = "warning", "Warning"
        MAINTENANCE = "maintenance", "Maintenance"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="gateways")
    name = models.CharField(max_length=180)
    gateway_id = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.OFFLINE, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=40, blank=True)
    os_version = models.CharField(max_length=80, blank=True)
    agent_version = models.CharField(max_length=80, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True, db_index=True)
    location = models.CharField(max_length=180, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("organization", "gateway_id")
        indexes = [models.Index(fields=["organization", "status"])]

    def __str__(self):
        return self.name
