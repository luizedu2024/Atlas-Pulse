from django.contrib import admin
from .models import AlertEvent, AlertRule

admin.site.register(AlertRule)
admin.site.register(AlertEvent)
