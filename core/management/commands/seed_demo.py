from datetime import timedelta
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from alerts.models import AlertEvent, AlertRule
from audit.models import AuditLog
from dashboards.models import Dashboard, DashboardWidget
from devices.models import Device
from gateways.models import Gateway
from organizations.models import Organization
from telemetry.models import TelemetryPoint


class Command(BaseCommand):
    help = "Create demo data for local Atlas Pulse development."

    def handle(self, *args, **options):
        org, _ = Organization.objects.get_or_create(
            slug="demo",
            defaults={"name": "Demo Manufacturing", "description": "Demo industrial tenant"},
        )
        User = get_user_model()
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@atlas.local", "organization": org, "role": "admin", "is_staff": True, "is_superuser": True},
        )
        if created:
            admin.set_password("admin123")
            admin.save()

        gateway, _ = Gateway.objects.get_or_create(
            organization=org,
            gateway_id="edge-001",
            defaults={"name": "Main Edge Gateway", "status": "online", "location": "Plant A", "agent_version": "0.1.0"},
        )
        specs = [
            ("motor-001", "Motor Line 1", "Motor", "online"),
            ("pump-014", "Cooling Pump", "Pump", "warning"),
            ("press-003", "Hydraulic Press", "Press", "offline"),
            ("oven-008", "Thermal Oven", "Oven", "online"),
        ]
        devices = []
        for device_id, name, dtype, status in specs:
            device, _ = Device.objects.get_or_create(
                organization=org,
                device_id=device_id,
                defaults={
                    "name": name,
                    "device_type": dtype,
                    "status": status,
                    "protocol": "MQTT",
                    "gateway": gateway,
                    "location": "Plant A",
                    "last_seen": timezone.now() - timedelta(minutes=random.randint(1, 90)),
                },
            )
            devices.append(device)

        rule, _ = AlertRule.objects.get_or_create(
            organization=org,
            name="Temperature above 80C",
            metric="temperature",
            defaults={"operator": ">", "threshold": 80, "severity": "critical"},
        )
        now = timezone.now()
        for device in devices:
            for hour in range(24, 0, -1):
                TelemetryPoint.objects.get_or_create(
                    organization=org,
                    device=device,
                    metric="temperature",
                    timestamp=now - timedelta(hours=hour),
                    defaults={"value": round(random.uniform(58, 86), 2), "unit": "C"},
                )
                TelemetryPoint.objects.get_or_create(
                    organization=org,
                    device=device,
                    metric="rpm",
                    timestamp=now - timedelta(hours=hour),
                    defaults={"value": random.randint(1200, 1560), "unit": "rpm"},
                )
        AlertEvent.objects.get_or_create(
            alert_rule=rule,
            device=devices[1],
            metric="temperature",
            status="active",
            defaults={"value": 84.2, "severity": "critical", "message": "Cooling Pump temperature exceeded threshold"},
        )
        dashboard, _ = Dashboard.objects.get_or_create(organization=org, name="Operations Overview", defaults={"is_default": True})
        DashboardWidget.objects.get_or_create(dashboard=dashboard, title="Telemetry - Last 24 hours", defaults={"widget_type": "line_chart"})
        AuditLog.objects.get_or_create(organization=org, user=admin, action="seed_demo", description="Demo workspace initialized")
        self.stdout.write(self.style.SUCCESS("Demo ready: admin / admin123"))
