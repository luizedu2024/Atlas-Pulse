from django.contrib import admin

from automations.models import AutomationRule, DeviceCommand


admin.site.register(AutomationRule)
admin.site.register(DeviceCommand)
