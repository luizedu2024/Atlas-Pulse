from rest_framework import decorators, response, status, viewsets

from alerts.models import AlertEvent, AlertRule
from api.serializers import (
    AlertEventSerializer,
    AlertRuleSerializer,
    DeviceCommandSerializer,
    DeviceSerializer,
    GatewaySerializer,
    TelemetryPointSerializer,
)
from automations.models import DeviceCommand
from devices.models import Device
from gateways.models import Gateway
from telemetry.models import TelemetryPoint


class TenantQuerySetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        organization = self.request.organization
        if queryset.model is AlertEvent:
            return queryset.filter(device__organization=organization)
        if queryset.model is DeviceCommand:
            return queryset.filter(device__organization=organization)
        return queryset.filter(organization=organization)

    def perform_create(self, serializer):
        if any(field.name == "organization" for field in serializer.Meta.model._meta.fields):
            serializer.save(organization=self.request.organization)
        else:
            serializer.save()


class DeviceViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    queryset = Device.objects.select_related("gateway", "organization")
    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        serializer.save(organization=self.request.organization)

    @decorators.action(detail=True, methods=["get"])
    def telemetry(self, request, pk=None):
        device = self.get_object()
        data = TelemetryPoint.objects.filter(device=device)[:250]
        return response.Response(TelemetryPointSerializer(data, many=True).data)

    @decorators.action(detail=True, methods=["post"])
    def commands(self, request, pk=None):
        device = self.get_object()
        serializer = DeviceCommandSerializer(data={**request.data, "device": device.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(requested_by=request.user)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class GatewayViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    queryset = Gateway.objects.select_related("organization")
    serializer_class = GatewaySerializer

    def perform_create(self, serializer):
        serializer.save(organization=self.request.organization)


class AlertRuleViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    queryset = AlertRule.objects.select_related("organization", "device")
    serializer_class = AlertRuleSerializer

    def perform_create(self, serializer):
        serializer.save(organization=self.request.organization)


class AlertEventViewSet(TenantQuerySetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = AlertEvent.objects.select_related("device", "alert_rule")
    serializer_class = AlertEventSerializer
