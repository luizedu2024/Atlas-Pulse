from django.core.management.base import BaseCommand

from integrations.mqtt.client import start_consumer


class Command(BaseCommand):
    help = "Subscribe to Atlas Pulse MQTT telemetry topics."

    def handle(self, *args, **options):
        start_consumer()
