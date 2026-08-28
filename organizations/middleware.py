from organizations.models import Organization


class ActiveOrganizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.organization = None
        if request.user.is_authenticated:
            memberships = request.user.memberships.filter(is_active=True).select_related("organization")
            active_id = request.session.get("active_organization_id")
            membership = memberships.filter(organization_id=active_id).first() if active_id else None
            membership = membership or memberships.first()
            if membership:
                request.organization = membership.organization
                request.session["active_organization_id"] = membership.organization_id
            request.organizations = Organization.objects.filter(memberships__user=request.user, memberships__is_active=True)
        return self.get_response(request)
