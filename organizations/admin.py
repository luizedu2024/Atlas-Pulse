from django.contrib import admin

from organizations.models import Organization, OrganizationMembership, UserInvitation


admin.site.register(Organization)
admin.site.register(OrganizationMembership)
admin.site.register(UserInvitation)
