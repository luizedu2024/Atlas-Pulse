from rest_framework.permissions import BasePermission, SAFE_METHODS


class TenantScopedPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request, "organization", None))

    def has_object_permission(self, request, view, obj):
        membership = request.user.memberships.filter(organization=request.organization, is_active=True).first()
        if request.method not in SAFE_METHODS and membership and membership.role == "viewer":
            return False
        organization = getattr(obj, "organization", None) or getattr(getattr(obj, "device", None), "organization", None)
        return organization == request.organization
