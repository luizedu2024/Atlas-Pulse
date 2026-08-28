import paho.mqtt.client as mqtt
from django.conf import settings

from integrations.mqtt.consumer import handle_message


def start_consumer():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    if settings.MQTT_USERNAME:
        client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)

    def on_connect(client, userdata, flags, reason_code, properties):
        client.subscribe("atlas/+/+/telemetry")

    def on_message(client, userdata, message):
        handle_message(message.topic, message.payload.decode("utf-8"))

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(settings.MQTT_HOST, settings.MQTT_PORT, 60)
    client.loop_forever()
