from django.contrib import admin
from .models import AutomationRule, DeviceCommand

admin.site.register(AutomationRule)
admin.site.register(DeviceCommand)
