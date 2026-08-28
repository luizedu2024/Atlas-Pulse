from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.forms import EmailAuthenticationForm, ProfileForm, RegistrationForm
from accounts.models import User
from accounts.tokens import make_email_token, read_email_token
from audit.services import audit
from organizations.models import OrganizationMembership


class AtlasLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = "registration/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        if not form.cleaned_data.get("remember_me"):
            self.request.session.set_expiry(0)
        audit(self.request, "login_success", description="User signed in")
        return response

    def get_success_url(self):
        user = self.request.user
        if not user.is_email_verified:
            return reverse("verify_email_required")
        if not user.memberships.filter(is_active=True).exists():
            return reverse("onboarding")
        return reverse("dashboard")


def register(request):
    invitation_token = request.GET.get("invitation", "")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_email_verified = False
            user.save()
            token = make_email_token(user)
            verify_url = request.build_absolute_uri(reverse("verify_email", args=[token]))
            send_mail(
                "Verify your Atlas Pulse email",
                f"Open this link to verify your email: {verify_url}",
                "noreply@atlaspulse.local",
                [user.email],
                fail_silently=True,
            )
            login(request, user, backend="accounts.auth.EmailOrUsernameBackend")
            audit(request, "user_registered", user, "Public registration completed")
            if invitation_token:
                request.session["pending_invitation_token"] = invitation_token
            return redirect("verify_email_required")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


def verify_email(request, token):
    try:
        data = read_email_token(token)
        user = User.objects.get(pk=data["user_id"], email=data["email"])
    except Exception:
        messages.error(request, "Invalid or expired verification link.")
        return redirect("verify_email_required")
    user.is_email_verified = True
    user.save(update_fields=["is_email_verified", "updated_at"])
    if request.user.is_authenticated and request.user == user:
        audit(request, "email_verified", user)
    messages.success(request, "Email verified successfully.")
    pending = request.session.get("pending_invitation_token")
    if pending:
        return redirect("accept_invitation", token=pending)
    return redirect("onboarding" if not user.memberships.filter(is_active=True).exists() else "dashboard")


@login_required
def verify_email_required(request):
    return render(request, "registration/verify_email_required.html")


@login_required
def onboarding(request):
    if not request.user.is_email_verified:
        return redirect("verify_email_required")
    if request.user.memberships.filter(is_active=True).exists():
        return redirect("dashboard")
    return render(request, "registration/onboarding.html")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    delete_blocked = False
    for membership in OrganizationMembership.objects.filter(user=request.user, role="admin", is_active=True):
        other_admins = membership.organization.memberships.filter(role="admin", is_active=True).exclude(user=request.user)
        if not other_admins.exists():
            delete_blocked = True
            break
    return render(request, "registration/profile.html", {"form": form, "delete_blocked": delete_blocked})
