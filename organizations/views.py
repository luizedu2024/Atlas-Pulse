import hashlib
import secrets
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from audit.services import audit
from organizations.forms import InvitationCreateForm, OrganizationCreateForm
from organizations.models import Organization, OrganizationMembership, UserInvitation
from organizations.permissions import can_manage_users


def hash_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


@login_required
def create_organization(request):
    if not request.user.is_email_verified:
        return redirect("verify_email_required")
    if request.method == "POST":
        form = OrganizationCreateForm(request.POST)
        if form.is_valid():
            organization = form.save()
            OrganizationMembership.objects.create(user=request.user, organization=organization, role="admin")
            request.session["active_organization_id"] = organization.id
            audit(request, "organization_created", organization, "Organization created from onboarding")
            return redirect("dashboard")
    else:
        form = OrganizationCreateForm()
    return render(request, "organizations/create.html", {"form": form})


@login_required
def switch_organization(request, pk):
    membership = get_object_or_404(
        OrganizationMembership,
        user=request.user,
        organization_id=pk,
        is_active=True,
    )
    request.session["active_organization_id"] = membership.organization_id
    audit(request, "organization_switched", membership.organization)
    return redirect(request.META.get("HTTP_REFERER") or "dashboard")


@login_required
def invite_user(request):
    if not can_manage_users(request.user, request.organization):
        return HttpResponseForbidden("Only organization administrators can invite users.")
    if request.method == "POST":
        form = InvitationCreateForm(request.POST)
        if form.is_valid():
            raw_token = secrets.token_urlsafe(32)
            invitation = form.save(commit=False)
            invitation.organization = request.organization
            invitation.invited_by = request.user
            invitation.token_hash = hash_token(raw_token)
            invitation.expires_at = timezone.now() + timedelta(days=7)
            invitation.save()
            accept_url = request.build_absolute_uri(reverse("accept_invitation", args=[raw_token]))
            messages.success(request, f"Invitation created: {accept_url}")
            audit(request, "invitation_created", invitation, f"Invitation sent to {invitation.email}")
            return redirect("invite_user")
    else:
        form = InvitationCreateForm()
    invitations = UserInvitation.objects.filter(organization=request.organization).order_by("-created_at")[:25]
    return render(request, "organizations/invite.html", {"form": form, "invitations": invitations})


def accept_invitation(request, token):
    invitation = get_object_or_404(UserInvitation, token_hash=hash_token(token))
    if invitation.status != "pending" or invitation.expires_at < timezone.now():
        invitation.status = "expired"
        invitation.save(update_fields=["status"])
        return render(request, "organizations/invitation_invalid.html")
    if not request.user.is_authenticated:
        request.session["pending_invitation_token"] = token
        return render(request, "organizations/accept_invitation_public.html", {"invitation": invitation, "token": token})
    if not request.user.is_email_verified:
        request.session["pending_invitation_token"] = token
        return redirect("verify_email_required")
    if request.user.email.lower() != invitation.email.lower():
        return HttpResponseForbidden("This invitation belongs to another email address.")
    OrganizationMembership.objects.get_or_create(
        user=request.user,
        organization=invitation.organization,
        defaults={"role": invitation.role},
    )
    invitation.status = "accepted"
    invitation.accepted_at = timezone.now()
    invitation.save(update_fields=["status", "accepted_at"])
    request.session["active_organization_id"] = invitation.organization_id
    audit(request, "invitation_accepted", invitation, f"Invitation accepted for {invitation.organization}")
    return redirect("dashboard")
