import hashlib
import secrets

from django.db import models


class Device(models.Model):
    class Status(models.TextChoices):
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"
        WARNING = "warning", "Warning"
        MAINTENANCE = "maintenance", "Maintenance"
        UNKNOWN = "unknown", "Unknown"

    class Protocol(models.TextChoices):
        MQTT = "MQTT", "MQTT"
        HTTP = "HTTP", "HTTP"
        MODBUS_TCP = "Modbus TCP", "Modbus TCP"
        MODBUS_RTU = "Modbus RTU", "Modbus RTU"
        OPC_UA = "OPC-UA", "OPC-UA"
        CUSTOM = "Custom", "Custom"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="devices")
    name = models.CharField(max_length=180)
    device_id = models.CharField(max_length=120)
    device_token_hash = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    device_type = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    firmware_version = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.UNKNOWN, db_index=True)
    protocol = models.CharField(max_length=30, choices=Protocol.choices, default=Protocol.MQTT, db_index=True)
    gateway = models.ForeignKey("gateways.Gateway", null=True, blank=True, on_delete=models.SET_NULL, related_name="devices")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=180, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("organization", "device_id")
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["organization", "protocol"]),
        ]

    def __str__(self):
        return self.name

    @staticmethod
    def hash_token(token):
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def rotate_token(self):
        token = secrets.token_urlsafe(32)
        self.device_token_hash = self.hash_token(token)
        self.save(update_fields=["device_token_hash", "updated_at"])
        return token
