from django.contrib.auth.models import AbstractUser
from django.db import models

from core.choices import SystemRole


class User(AbstractUser):
    # name, acitve
    role = models.CharField(
        max_length=20,
        choices=SystemRole.choices,
        default=SystemRole.VOLUNTEER,
    )

    def __str__(self):
        return self.username

    @property
    def is_sys_admin(self) -> bool:
        return self.role == SystemRole.SYS_ADMIN

    @property
    def is_manager(self) -> bool:
        return self.role == SystemRole.MANAGER

    @property
    def is_staff_role(self) -> bool:
        return self.role in {SystemRole.STAFF, SystemRole.MANAGER, SystemRole.SYS_ADMIN}