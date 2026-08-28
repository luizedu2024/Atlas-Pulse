from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from alerts.models import AlertEvent
from devices.models import Device
from telemetry.models import TelemetryPoint


@login_required
def device_list(request):
    devices = Device.objects.filter(organization=request.user.organization).select_related("gateway")
    search = request.GET.get("q", "")
    if search:
        devices = devices.filter(name__icontains=search)
    for field in ("status", "protocol", "gateway"):
        value = request.GET.get(field)
        if value:
            devices = devices.filter(**{field: value})
    return render(request, "devices/list.html", {"devices": devices})


@login_required
def device_detail(request, pk):
    device = get_object_or_404(
        Device.objects.select_related("gateway", "organization"),
        pk=pk,
        organization=request.user.organization,
    )
    since = timezone.now() - timedelta(hours=24)
    telemetry = TelemetryPoint.objects.filter(device=device, timestamp__gte=since).order_by("timestamp")
    alerts = AlertEvent.objects.filter(device=device).select_related("alert_rule")[:8]
    return render(request, "devices/detail.html", {"device": device, "telemetry": telemetry, "alerts": alerts})
