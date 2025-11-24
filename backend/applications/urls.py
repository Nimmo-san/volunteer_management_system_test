from rest_framework.routers import DefaultRouter
from .views import OpportunityViewSet, ApplicationViewSet, InterviewViewSet

router = DefaultRouter()
router.register("opportunities", OpportunityViewSet, basename="opportunity")
router.register("applications", ApplicationViewSet, basename="application")
router.register("interviews", InterviewViewSet, basename="interview")

urlpatterns = router.urls
