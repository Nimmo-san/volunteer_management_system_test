from rest_framework.routers import DefaultRouter
from .views import PlacementViewSet, ShiftViewSet

router = DefaultRouter()
router.register("placements", PlacementViewSet, basename="placement")
router.register("shifts", ShiftViewSet, basename="shift")

urlpatterns = router.urls
