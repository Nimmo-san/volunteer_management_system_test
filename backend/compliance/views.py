from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from accounts.models import SystemRole
from volunteers.models import VolunteerProfile
from .models import ComplianceCheck
from .serializers import ComplianceCheckSerializer


class CompliancePermission(permissions.BasePermission):
    """
    - Volunteers: can view only their own checks (GET/HEAD/OPTIONS).
    - Staff/manager/sys_admin: full access.
    """

    def has_permission(self, request, view): # type: ignore
        user = request.user
        return bool(user and user.is_authenticated)

    def has_object_permission(self, request, view, obj: ComplianceCheck):  # type: ignore
        user = request.user

        if user.role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return True

        if user.role == SystemRole.VOLUNTEER:
            if request.method in permissions.SAFE_METHODS:
                return obj.volunteer.user_id == user.id
            return False

        return False


class ComplianceCheckViewSet(viewsets.ModelViewSet):
    queryset = ComplianceCheck.objects.select_related(
        "volunteer",
        "volunteer__user",
    ).all()
    serializer_class = ComplianceCheckSerializer
    permission_classes = [permissions.IsAuthenticated, CompliancePermission]

    def get_queryset(self):  # type: ignore
        user = self.request.user

        role = getattr(user, "role", None)
        if role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return self.queryset

        # TODO: Avoid direct attribute access on user (AbstractUser/AnonymousUser) and
        # fetch the VolunteerProfile via a queryset so static analysis won't complain.
        # volunteer_profile = VolunteerProfile.objects.filter(user=user).first()
        if role == SystemRole.VOLUNTEER:
            try:
                volunteer_profile = user.volunteer_profile
            except VolunteerProfile.DoesNotExist:
                return ComplianceCheck.objects.none()
            return self.queryset.filter(volunteer=volunteer_profile)

        return ComplianceCheck.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        role = getattr(user, "role", None)
        if role not in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            raise PermissionDenied("Only staff may create compliance checks.")

        # Volunteer is provided via payload; we trust serializer's FK validation
        serializer.save()
