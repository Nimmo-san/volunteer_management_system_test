from rest_framework.routers import DefaultRouter
from .views import VolunteerProfileViewSet


router = DefaultRouter()
router.register("profiles", VolunteerProfileViewSet, basename="volunteer-profile")
urlpatterns = router.urls