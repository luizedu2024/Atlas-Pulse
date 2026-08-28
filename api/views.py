from rest_framework import decorators, response, viewsets

from alerts.models import AlertEvent, AlertRule
from automations.models import DeviceCommand
from devices.models import Device
from gateways.models import Gateway
from telemetry.models import TelemetryPoint
from .permissions import TenantScopedPermission
from .serializers import (
    AlertEventSerializer,
    AlertRuleSerializer,
    DeviceCommandSerializer,
    DeviceSerializer,
    GatewaySerializer,
    TelemetryPointSerializer,
)


class TenantViewSet(viewsets.ModelViewSet):
    permission_classes = [TenantScopedPermission]

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)


class DeviceViewSet(TenantViewSet):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(organization=self.request.user.organization).select_related("gateway")

    @decorators.action(detail=True, methods=["get"])
    def telemetry(self, request, pk=None):
        points = TelemetryPoint.objects.filter(device=self.get_object())[:500]
        return response.Response(TelemetryPointSerializer(points, many=True).data)

    @decorators.action(detail=True, methods=["post"])
    def commands(self, request, pk=None):
        serializer = DeviceCommandSerializer(data={**request.data, "device": self.get_object().pk})
        serializer.is_valid(raise_exception=True)
        serializer.save(requested_by=request.user)
        return response.Response(serializer.data, status=201)


class GatewayViewSet(TenantViewSet):
    serializer_class = GatewaySerializer

    def get_queryset(self):
        return Gateway.objects.filter(organization=self.request.user.organization)


class AlertRuleViewSet(TenantViewSet):
    serializer_class = AlertRuleSerializer

    def get_queryset(self):
        return AlertRule.objects.filter(organization=self.request.user.organization)


class AlertEventViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [TenantScopedPermission]
    serializer_class = AlertEventSerializer

    def get_queryset(self):
        return AlertEvent.objects.filter(device__organization=self.request.user.organization).select_related("device", "alert_rule")
