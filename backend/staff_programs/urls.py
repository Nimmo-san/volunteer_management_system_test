from rest_framework.routers import DefaultRouter
from .views import StaffProfileViewSet, ProgramRequestViewSet


router = DefaultRouter()
router.register("profiles", StaffProfileViewSet, basename="staff-profile")
router.register("program-request", ProgramRequestViewSet, basename="program-request")

urlpatterns = router.urls