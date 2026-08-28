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
    return redirect("dashboard" if request.user.is_authenticated else "login")


@login_required
def dashboard(request):
    org = request.user.organization
    devices = Device.objects.filter(organization=org).select_related("gateway")
    gateways = Gateway.objects.filter(organization=org)
    alerts = AlertEvent.objects.filter(device__organization=org).select_related("device", "alert_rule")
    since = timezone.now() - timedelta(hours=24)
    points = TelemetryPoint.objects.filter(organization=org, timestamp__gte=since).order_by("timestamp")
    chart_labels = [p.timestamp.strftime("%H:%M") for p in points if p.metric == "temperature"][-24:]
    chart_values = [p.value for p in points if p.metric == "temperature"][-24:]
    context = {
        "devices_online": devices.filter(status="online").count(),
        "devices_offline": devices.filter(status="offline").count(),
        "gateways_online": gateways.filter(status="online").count(),
        "active_alerts": alerts.filter(status="active").count(),
        "device_status": devices.values("status").annotate(total=Count("id")),
        "recent_alerts": alerts[:6],
        "latest_activity": AuditLog.objects.filter(organization=org)[:8],
        "chart_labels": chart_labels,
        "chart_values": chart_values,
    }
    return render(request, "core/dashboard.html", context)
