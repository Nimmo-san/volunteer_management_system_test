from rest_framework.routers import DefaultRouter
from .views import ComplianceCheckViewSet

router = DefaultRouter()
router.register("checks", ComplianceCheckViewSet, basename="compliance-check")

urlpatterns = router.urls
