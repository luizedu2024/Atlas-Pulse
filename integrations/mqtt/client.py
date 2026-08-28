import logging

import paho.mqtt.client as mqtt
from django.conf import settings

from .consumer import handle_telemetry_message

logger = logging.getLogger(__name__)


def start_mqtt_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if settings.MQTT_USERNAME:
        client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

    def on_connect(client, userdata, flags, reason_code, properties):
        logger.info("MQTT connected: %s", reason_code)
        client.subscribe("atlas/+/+/telemetry")

    def on_message(client, userdata, message):
        try:
            handle_telemetry_message(message.topic, message.payload.decode("utf-8"))
        except Exception:
            logger.exception("Failed to process MQTT message on %s", message.topic)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(settings.MQTT_HOST, settings.MQTT_PORT, 60)
    client.loop_forever()
