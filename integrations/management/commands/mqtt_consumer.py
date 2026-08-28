from django.core.management.base import BaseCommand

from integrations.mqtt.client import start_mqtt_client


class Command(BaseCommand):
    help = "Subscribe to Atlas Pulse MQTT telemetry topics."

    def handle(self, *args, **options):
        start_mqtt_client()
