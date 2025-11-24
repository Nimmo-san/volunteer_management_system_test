from django.db import models
from django.conf import settings


class StaffProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )

    department = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, blank=True)

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.username} ({self.department})"

class ProgramRequest(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("approved", "Approved"),
        ("active", "Active"),
        ("closed", "Closed"),
    ]

    created_by = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="created_programs",
    )
    primary_contact = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name="primary_programs",
    )
    secondary_contacts = models.ManyToManyField(
        StaffProfile,
        # on_delete=models.CASCADE,
        related_name="secondary_programs",
        blank=True,
        # null=True
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    department = models.CharField(max_length=255, blank=True)
    volunteers_needed = models.PositiveIntegerField(default=1)

    # simple eligibility flag for now
    eligibility_status = models.CharField(
        max_length=50,
        default="pending", # -> pending / eligible / ineligible
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    approval_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.get_status_display()})" # type: ignore
    