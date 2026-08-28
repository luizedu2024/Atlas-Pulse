from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils import timezone

from alerts.models import AlertEvent
from audit.models import AuditLog
from devices.models import Device
from gateways.models import Gateway
from telemetry.models import TelemetryPoint


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "core/landing.html")


@login_required
def dashboard(request):
    if not request.user.is_email_verified:
        return redirect("verify_email_required")
    if not request.organization:
        return redirect("onboarding")
    devices = Device.objects.filter(organization=request.organization).select_related("gateway")
    gateways = Gateway.objects.filter(organization=request.organization)
    alerts = AlertEvent.objects.filter(device__organization=request.organization).select_related("device", "alert_rule")
    since = timezone.now() - timedelta(hours=24)
    temperature = TelemetryPoint.objects.filter(
        organization=request.organization,
        metric="temperature",
        timestamp__gte=since,
    ).order_by("timestamp")
    context = {
        "devices_online": devices.filter(status="online").count(),
        "devices_offline": devices.filter(status="offline").count(),
        "gateways_online": gateways.filter(status="online").count(),
        "active_alerts": alerts.filter(status="active").count(),
        "device_status": devices.values("status").annotate(total=Count("id")),
        "recent_alerts": alerts[:6],
        "latest_activity": AuditLog.objects.filter(organization=request.organization)[:8],
        "chart_labels": [p.timestamp.strftime("%H:%M") for p in temperature][-32:],
        "chart_values": [p.value for p in temperature][-32:],
    }
    return render(request, "core/dashboard.html", context)
