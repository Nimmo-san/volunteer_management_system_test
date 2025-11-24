from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from accounts.models import SystemRole
from volunteers.models import VolunteerProfile
from .models import Placement, Shift
from .serializers import PlacementSerializer, ShiftSerializer


# TODO: Dont access static attributes directly, will get on it

class PlacementPermission(permissions.BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj: Placement):  # type: ignore
        user = request.user

        if user.role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return True

        if user.role == SystemRole.VOLUNTEER:
            if request.method in permissions.SAFE_METHODS:
                return obj.volunteer.user_id == user.id
            return False

        return False


class ShiftPermission(permissions.BasePermission):
    def has_permission(self, request, view):  # type: ignore
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj: Shift):  # type: ignore
        user = request.user

        if user.role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return True

        if user.role == SystemRole.VOLUNTEER:
            if request.method in permissions.SAFE_METHODS:
                return obj.placement.volunteer.user_id == user.id
            return False

        return False


class PlacementViewSet(viewsets.ModelViewSet):
    queryset = Placement.objects.select_related(
        "volunteer",
        "volunteer__user",
        "opportunity",
        "supervisor",
        "supervisor__user",
    ).all()
    serializer_class = PlacementSerializer
    permission_classes = [permissions.IsAuthenticated, PlacementPermission]

    def get_queryset(self):  # type: ignore
        user = self.request.user

        if user.role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return self.queryset

        if user.role == SystemRole.VOLUNTEER:
            try:
                volunteer_profile = user.volunteer_profile
            except VolunteerProfile.DoesNotExist:
                return Placement.objects.none()
            return self.queryset.filter(volunteer=volunteer_profile)

        return Placement.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role not in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            raise PermissionDenied("Only staff may create placements.")

        serializer.save()


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.select_related(
        "placement",
        "placement__volunteer",
        "placement__volunteer__user",
    ).all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated, ShiftPermission]

    def get_queryset(self):  # type: ignore
        user = self.request.user

        if user.role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return self.queryset

        if user.role == SystemRole.VOLUNTEER:
            try:
                volunteer_profile = user.volunteer_profile
            except VolunteerProfile.DoesNotExist:
                return Shift.objects.none()
            return self.queryset.filter(
                placement__volunteer=volunteer_profile
            )

        return Shift.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role not in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            raise PermissionDenied("Only staff may create shifts.")

        serializer.save()
