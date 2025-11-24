from django.db import models
from django.conf import settings

from core.choices import ApplicationStatus
from volunteers.models import VolunteerProfile
from staff_programs.models import ProgramRequest


class Opportunity(models.Model):
    program = models.ForeignKey(
        ProgramRequest,
        on_delete=models.CASCADE,
        related_name="opportunities",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    # number of volunteers needed
    positions = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self) -> str:
        return f"{self.title} ({'active' if self.is_active else 'inactive'})"
    

class Application(models.Model):
    #volunteer, opportunity, application status, submitted date/time, updated date/time, internal notes maybe
    volunteer = models.ForeignKey(
        VolunteerProfile,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.NEW,
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # internal notes, rejection reasons, etc.
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-submitted_at"]
        unique_together = ("volunteer", "opportunity")

    def __str__(self) -> str:
        return f"{self.volunteer.user.username} -> {self.opportunity.title} ({self.status})"


class Interview(models.Model):
    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="interview",
    )
    scheduled_at = models.DateTimeField()
    interviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interviews",
    )

    outcome = models.CharField(
        max_length=50,
        blank=True,  # optionally use another TextChoices later
    )
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Interview for {self.application}"