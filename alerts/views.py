from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from alerts.models import AlertEvent


@login_required
def alert_list(request):
    if not request.organization:
        return redirect("onboarding")
    events = AlertEvent.objects.filter(device__organization=request.organization).select_related("device", "alert_rule")
    return render(request, "alerts/list.html", {
        "events": events[:100],
        "critical": events.filter(severity="critical", status="active").count(),
        "warning": events.filter(severity="warning", status="active").count(),
        "info": events.filter(severity="info", status="active").count(),
    })
