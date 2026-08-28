import json
from django.utils.dateparse import parse_datetime


def parse_topic(topic):
    parts = topic.split("/")
    if len(parts) != 4 or parts[0] != "atlas" or parts[3] != "telemetry":
        raise ValueError("Expected topic atlas/{organization}/{device}/telemetry")
    return parts[1], parts[2]


def parse_payload(payload):
    data = json.loads(payload)
    if "metrics" not in data or not isinstance(data["metrics"], dict):
        raise ValueError("Payload must include metrics object")
    if data.get("timestamp"):
        data["timestamp"] = parse_datetime(data["timestamp"])
    return data
