from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts import views as account_views
from core import views as core_views
from organizations import views as organization_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", core_views.home, name="home"),
    path("dashboard/", core_views.dashboard, name="dashboard"),
    path("register/", account_views.register, name="register"),
    path("verify-email/<str:token>/", account_views.verify_email, name="verify_email"),
    path("verify-email-required/", account_views.verify_email_required, name="verify_email_required"),
    path("onboarding/", account_views.onboarding, name="onboarding"),
    path("profile/", account_views.profile, name="profile"),
    path("devices/", include("devices.urls")),
    path("alerts/", include("alerts.urls")),
    path("organizations/", include("organizations.urls")),
    path("invitations/accept/<str:token>/", organization_views.accept_invitation, name="accept_invitation"),
    path("login/", account_views.AtlasLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
    path("api/v1/", include("api.urls")),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
