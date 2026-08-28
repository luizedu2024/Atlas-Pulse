from django.urls import path

from alerts import views

urlpatterns = [path("", views.alert_list, name="alert_list")]
