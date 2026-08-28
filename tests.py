import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from alerts.models import AlertEvent, AlertRule
from core.services.telemetry import TelemetryService
from devices.models import Device
from organizations.models import Organization


@pytest.fixture
def org(db):
    return Organization.objects.create(name="ACME", slug="acme")


@pytest.fixture
def user(org):
    User = get_user_model()
    return User.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="pass",
        organization=org,
        role="admin",
    )


@pytest.mark.django_db
def test_login_redirects_to_dashboard(client, user):
    response = client.post(reverse("login"), {"username": "admin@example.com", "password": "pass"})
    assert response.status_code == 302
    assert response.url == reverse("dashboard")


@pytest.mark.django_db
def test_tenant_isolation_on_devices_api(client, user, org):
    other = Organization.objects.create(name="Other", slug="other")
    Device.objects.create(organization=org, name="Visible", device_id="visible")
    Device.objects.create(organization=other, name="Hidden", device_id="hidden")
    client.force_login(user)
    response = client.get("/api/v1/devices/")
    names = [item["name"] for item in response.json()]
    assert names == ["Visible"]


@pytest.mark.django_db
def test_telemetry_ingestion_triggers_alert(org):
    device = Device.objects.create(organization=org, name="Motor", device_id="motor-001")
    AlertRule.objects.create(organization=org, name="Hot", metric="temperature", operator=">", threshold=80, severity="critical")
    TelemetryService.ingest_payload(org, "motor-001", {
        "timestamp": timezone.now(),
        "metrics": {"temperature": {"value": 82, "unit": "C"}},
    })
    assert AlertEvent.objects.filter(device=device, severity="critical").exists()
