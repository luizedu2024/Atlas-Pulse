from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AlertEventViewSet, AlertRuleViewSet, DeviceViewSet, GatewayViewSet

router = DefaultRouter()
router.register("devices", DeviceViewSet, basename="device")
router.register("gateways", GatewayViewSet, basename="gateway")
router.register("alert-rules", AlertRuleViewSet, basename="alert-rule")
router.register("alerts", AlertEventViewSet, basename="alert")

urlpatterns = [path("", include(router.urls))]
