from rest_framework import serializers

from alerts.models import AlertEvent, AlertRule
from automations.models import DeviceCommand
from devices.models import Device
from gateways.models import Gateway
from telemetry.models import TelemetryPoint


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        exclude = ["device_token_hash"]
        read_only_fields = ["organization"]


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = "__all__"
        read_only_fields = ["organization"]


class TelemetryPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryPoint
        fields = "__all__"
        read_only_fields = ["organization"]


class AlertRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRule
        fields = "__all__"
        read_only_fields = ["organization"]


class AlertEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertEvent
        fields = "__all__"


class DeviceCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCommand
        fields = "__all__"
        read_only_fields = ["requested_by"]
