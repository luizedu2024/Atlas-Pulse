from django.urls import path

from organizations import views

urlpatterns = [
    path("create/", views.create_organization, name="organization_create"),
    path("switch/<int:pk>/", views.switch_organization, name="organization_switch"),
    path("invite/", views.invite_user, name="invite_user"),
]
