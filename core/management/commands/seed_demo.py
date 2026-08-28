from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from alerts.models import AlertEvent, AlertRule
from devices.models import Device
from gateways.models import Gateway
from organizations.models import Organization, OrganizationMembership
from telemetry.models import TelemetryPoint


class Command(BaseCommand):
    help = "Seed Atlas Pulse demo data"

    def handle(self, *args, **options):
        org, _ = Organization.objects.get_or_create(
            slug="demo",
            defaults={"name": "Demo Industrial", "description": "Demo tenant", "timezone": "America/Sao_Paulo"},
        )
        user, created = User.objects.get_or_create(
            email="admin@atlaspulse.local",
            defaults={"full_name": "Atlas Admin", "is_staff": True, "is_superuser": True, "is_email_verified": True},
        )
        if created:
            user.set_password("admin12345")
            user.save()
        OrganizationMembership.objects.get_or_create(user=user, organization=org, defaults={"role": "admin"})
        gateway, _ = Gateway.objects.get_or_create(
            organization=org,
            gateway_id="gw-001",
            defaults={"name": "Gateway Line A", "status": "online", "location": "Plant A"},
        )
        device, _ = Device.objects.get_or_create(
            organization=org,
            device_id="motor-001",
            defaults={
                "name": "Motor 001",
                "device_type": "Motor",
                "status": "online",
                "protocol": "MQTT",
                "gateway": gateway,
                "location": "Line A",
                "firmware_version": "1.0.0",
                "last_seen": timezone.now(),
            },
        )
        rule, _ = AlertRule.objects.get_or_create(
            organization=org,
            device=device,
            metric="temperature",
            defaults={"name": "Temperature above 80C", "operator": ">", "threshold": 80, "severity": "critical"},
        )
        now = timezone.now()
        for idx in range(24):
            TelemetryPoint.objects.get_or_create(
                organization=org,
                device=device,
                metric="temperature",
                timestamp=now - timedelta(hours=23 - idx),
                defaults={"value": 62 + idx * 0.8, "unit": "C"},
            )
        AlertEvent.objects.get_or_create(
            alert_rule=rule,
            device=device,
            metric="temperature",
            value=84.4,
            defaults={"severity": "critical", "message": "Temperature above 80C: temperature 84.4C > 80"},
        )
        self.stdout.write(self.style.SUCCESS("Demo seeded. Login: admin@atlaspulse.local / admin12345"))
