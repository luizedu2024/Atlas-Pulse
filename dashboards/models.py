from django.db import models


class Dashboard(models.Model):
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="dashboards")
    name = models.CharField(max_length=180)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class DashboardWidget(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name="widgets")
    title = models.CharField(max_length=180)
    widget_type = models.CharField(max_length=60)
    config = models.JSONField(default=dict, blank=True)
    position = models.PositiveIntegerField(default=0)
