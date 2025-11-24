from django.db import models

from volunteers.models import VolunteerProfile
from staff_programs.models import StaffProfile
from applications.models import Opportunity
from core.choices import ShiftStatus




"""
Necessary to link:
- Placements -> StaffProfile, VolunteerProfile, Opportunity
- Shifts -> Placement + ShiftStatus
"""

class Placement(models.Model):
    volunteer = models.ForeignKey(
        VolunteerProfile,
        on_delete=models.CASCADE,
        related_name="placements",
    )
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.PROTECT,
        related_name="placements",
    )
    supervisor = models.ForeignKey(
        StaffProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervised_placements",
    )

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    hours_per_week = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self) -> str:
        return f"{self.volunteer.user.username} @ {self.opportunity.title}"


class Shift(models.Model):
    placement = models.ForeignKey(
        Placement,
        on_delete=models.CASCADE,
        related_name="shifts",
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)

    status = models.CharField(
        max_length=20,
        choices=ShiftStatus.choices,
        default=ShiftStatus.SCHEDULED,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start"]

    def __str__(self) -> str:
        return f"{self.placement} [{self.start} - {self.end}] ({self.status})"
