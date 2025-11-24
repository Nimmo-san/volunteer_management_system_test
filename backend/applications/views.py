from django.db import models
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from accounts.models import SystemRole
from volunteers.models import VolunteerProfile
from staff_programs.models import StaffProfile
from core.choices import ApplicationStatus
from .models import Opportunity, Application, Interview
from .serializers import (
    OpportunitySerializer,
    ApplicationSerializer,
    InterviewSerializer,
)


class IsStaffLike(permissions.BasePermission):
    """
    STAFF / MANAGER / SYS_ADMIN.
    """

    def has_permission(self, request, view): # type: ignore
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}
        )


class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.select_related("program", "program__created_by").all()
    serializer_class = OpportunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self): # type: ignore
        user = self.request.user

        role = getattr(user, "role", None)
        # Volunteers see only active opportunities
        if role == SystemRole.VOLUNTEER:
            return self.queryset.filter(is_active=True)

        # Staff / managers see everything
        if role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return self.queryset

        return Opportunity.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        role = getattr(user, "role", None)
        if role not in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            raise PermissionDenied("Only staff can create opportunities.")

        # optional: enforce that program belongs to this staff
        serializer.save()


class ApplicationPermission(permissions.BasePermission):
    """
    - Volunteers: only their own applications.
    - Staff-like: can see all.
    """

    def has_permission(self, request, view): # type: ignore
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj: Application): # type: ignore
        user = request.user
        role = getattr(user, "role", None)
        if role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return True

        if role == SystemRole.VOLUNTEER:
            # Compare the related User's id; guard if the volunteer has no related user.
            volunteer_user = getattr(obj.volunteer, "user", None)
            if volunteer_user is None:
                return False
            return volunteer_user.id == user.id

        return False


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related(
        "volunteer",
        "volunteer__user",
        "opportunity",
        "opportunity__program",
    ).all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, ApplicationPermission]

    def get_queryset(self): # type: ignore
        user = self.request.user

        role = getattr(user, "role", None)
        if role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return self.queryset

        if role == SystemRole.VOLUNTEER:
            try:
                volunteer_profile = getattr(user, "volunteer_profile", None)
            except VolunteerProfile.DoesNotExist:
                return Application.objects.none()
            return self.queryset.filter(volunteer=volunteer_profile)

        return Application.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        role = getattr(user, "role", None)
        if role != SystemRole.VOLUNTEER:
            raise PermissionDenied("Only volunteers can create applications.")

        try:
            volunteer_profile = getattr(user, "volunteer_profile", None)
        except VolunteerProfile.DoesNotExist:
            raise PermissionDenied("Volunteer profile not found.")

        opportunity = serializer.validated_data["opportunity"]
        if not opportunity.is_active:
            raise PermissionDenied("Cannot apply to an inactive opportunity.")

        serializer.save(
            volunteer=volunteer_profile,
            status=ApplicationStatus.NEW,
        )

    def perform_update(self, serializer):
        """
        Volunteers cannot change status; staff can.
        We enforce this at the view level.
        """
        user = self.request.user
        instance: Application = self.get_object()

        if user.role == SystemRole.VOLUNTEER:
            # strip status from validated data
            serializer.validated_data.pop("status", None)
            serializer.save(status=instance.status)
            return

        # staff-like can update everything
        serializer.save()


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.select_related(
        "application",
        "application__volunteer",
        "application__volunteer__user",
    ).all()
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffLike]

    def perform_create(self, serializer):
        # Optionally enforce that the interviewer is the current user
        if "interviewer" not in serializer.validated_data:
            serializer.save(interviewer=self.request.user)
        else:
            serializer.save()
