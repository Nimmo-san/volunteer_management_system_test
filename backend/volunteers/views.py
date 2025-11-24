from rest_framework import viewsets, permissions
from .models import VolunteerProfile
from .serializers import VolunteerProfileSerializer
from accounts.models import SystemRole


class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:  # type: ignore[override]
        user = request.user

        if not user.is_authenticated:
            return False

        # Staff-like roles can see any volunteer, not sure about sys_admin
        if user.role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return True

        # Volunteers can only see their own profile
        return obj.user == user


class VolunteerProfileViewSet(viewsets.ModelViewSet):
    queryset = VolunteerProfile.objects.all()
    serializer_class = VolunteerProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self): # type: ignore[override]
        user = self.request.user

        # using getattr(user, "role", None)
        if getattr(user, "role", None) in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}:
            return VolunteerProfile.objects.all()

        return VolunteerProfile.objects.filter(user=user)
