def active_membership(user, organization):
    if not user.is_authenticated or not organization:
        return None
    return user.memberships.filter(organization=organization, is_active=True).first()


def role(user, organization):
    membership = active_membership(user, organization)
    return membership.role if membership else None


def can_manage_users(user, organization):
    return role(user, organization) == "admin"


def can_manage_devices(user, organization):
    return role(user, organization) in {"admin", "engineer"}


def can_view_telemetry(user, organization):
    return role(user, organization) in {"admin", "engineer", "operator", "viewer"}


def can_manage_alerts(user, organization):
    return role(user, organization) in {"admin", "engineer"}


def can_execute_commands(user, organization):
    return role(user, organization) in {"admin", "engineer", "operator"}
