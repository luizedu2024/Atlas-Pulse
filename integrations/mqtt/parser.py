import json

from django.utils.dateparse import parse_datetime


def parse_topic(topic):
    parts = topic.split("/")
    if len(parts) != 4 or parts[0] != "atlas" or parts[3] != "telemetry":
        raise ValueError("Topic must match atlas/{organization}/{device}/telemetry")
    return parts[1], parts[2]


def parse_payload(payload):
    data = json.loads(payload)
    if data.get("timestamp"):
        data["timestamp"] = parse_datetime(data["timestamp"])
    if not isinstance(data.get("metrics"), dict):
        raise ValueError("Payload must include a metrics object")
    return data
