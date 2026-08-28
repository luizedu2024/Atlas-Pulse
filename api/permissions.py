from rest_framework.permissions import BasePermission, SAFE_METHODS


class TenantScopedPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.organization_id)

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS and request.user.role == "viewer":
            return False
        organization = getattr(obj, "organization", None) or getattr(getattr(obj, "device", None), "organization", None)
        return organization == request.user.organization
