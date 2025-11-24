from django.db import models
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from accounts.models import SystemRole
from .models import StaffProfile, ProgramRequest
from .serializers import StaffProfileSerializer, ProgramRequestSerializer


# TODO: note to self, consider taking away sys admin access to volunteers private info
class IsStaffOrManager(permissions.BasePermission):
    """
    Only allow authenticated users with STAFF / MANAGER / SYS_ADMIN roles.
    """

    def has_permission(self, request, view): # type: ignore
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}
        )


class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.select_related("user").all()
    serializer_class = StaffProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrManager]

    def get_queryset(self): # type: ignore
        user = self.request.user

        if getattr(user, "role", None) in {SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return StaffProfile.objects.select_related("user").all()

        # normal staff: only their own profile
        return StaffProfile.objects.select_related("user").filter(user=user)


class ProgramRequestViewSet(viewsets.ModelViewSet):
    queryset = ProgramRequest.objects.select_related(
        "created_by",
        "primary_contact",
        "created_by__user",
        "primary_contact__user",
    ).prefetch_related("secondary_contacts")
    serializer_class = ProgramRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrManager]

    def perform_create(self, serializer):
        user = self.request.user
        try:
            staff_profile = getattr(user, "staff_profile", None)
        except StaffProfile.DoesNotExist:
            raise PermissionDenied("Staff profile not found for this user.")

        department = getattr(staff_profile, "department", None)
        serializer.save(
            created_by=staff_profile,
            department=department or serializer.validated_data.get("department", ""),
        )

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()

        if user.role in {SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return qs

        try:
            staff_profile = user.staff_profile
        except StaffProfile.DoesNotExist:
            return ProgramRequest.objects.none()

        return qs.filter(
            models.Q(created_by=staff_profile)
            | models.Q(primary_contact=staff_profile)
            | models.Q(secondary_contacts=staff_profile)
        ).distinct()
