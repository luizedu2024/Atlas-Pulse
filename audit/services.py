from audit.models import AuditLog


def audit(request, action, obj=None, description=""):
    user = getattr(request, "user", None)
    organization = getattr(request, "organization", None)
    AuditLog.objects.create(
        organization=organization,
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        object_type=obj.__class__.__name__ if obj else "",
        object_id=str(getattr(obj, "pk", "")) if obj else "",
        description=description,
        ip_address=request.META.get("REMOTE_ADDR"),
    )
