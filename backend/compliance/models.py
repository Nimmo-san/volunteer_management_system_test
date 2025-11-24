from django.db import models

from core.choices import CheckType, CheckStatus
from volunteers.models import VolunteerProfile


class ComplianceCheck(models.Model):
    volunteer = models.ForeignKey(
        VolunteerProfile,
        on_delete=models.CASCADE,
        related_name="compliance_checks",
    )

    check_type = models.CharField(
        max_length=50,
        choices=CheckType.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=CheckStatus.choices,
        default=CheckStatus.PENDING,
    )

    details = models.TextField(
        blank=True,
        help_text="Optional notes, e.g. reference contact, RTW document type, etc.",
    )

    # e.g. expiry for DBS or RTW if relevant
    expires_at = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["volunteer", "check_type"]
        unique_together = ("volunteer", "check_type")

    def __str__(self) -> str:
        return f"{self.volunteer.user.username} - {self.check_type} ({self.status})"
