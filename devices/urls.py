from django.urls import path

from devices import views

urlpatterns = [
    path("", views.device_list, name="device_list"),
    path("<int:pk>/", views.device_detail, name="device_detail"),
]
