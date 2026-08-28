from rest_framework.routers import DefaultRouter

from api.views import AlertEventViewSet, AlertRuleViewSet, DeviceViewSet, GatewayViewSet

router = DefaultRouter()
router.register("devices", DeviceViewSet)
router.register("gateways", GatewayViewSet)
router.register("alert-rules", AlertRuleViewSet)
router.register("alerts", AlertEventViewSet)

urlpatterns = router.urls
