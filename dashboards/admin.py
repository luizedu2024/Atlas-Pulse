from django.contrib import admin

from dashboards.models import Dashboard, DashboardWidget


admin.site.register(Dashboard)
admin.site.register(DashboardWidget)
