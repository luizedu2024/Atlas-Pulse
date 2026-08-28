import operator

from alerts.models import AlertEvent, AlertRule


OPS = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}


class AlertService:
    @classmethod
    def evaluate_point(cls, point):
        rules = AlertRule.objects.filter(
            organization=point.organization,
            metric=point.metric,
            enabled=True,
        ).filter(device__isnull=True) | AlertRule.objects.filter(
            organization=point.organization,
            device=point.device,
            metric=point.metric,
            enabled=True,
        )
        events = []
        for rule in rules.distinct():
            if OPS[rule.operator](point.value, rule.threshold):
                events.append(AlertEvent.objects.create(
                    alert_rule=rule,
                    device=point.device,
                    metric=point.metric,
                    value=point.value,
                    severity=rule.severity,
                    message=f"{rule.name}: {point.metric} {point.value:g}{point.unit} {rule.operator} {rule.threshold:g}",
                ))
        return events
