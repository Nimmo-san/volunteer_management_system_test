from django.conf import settings
from django.db import models


class VolunteerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="volunteer_profile"
    )

    # may need to change max_length
    phone = models.CharField(max_length=32, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    role_preference = models.TextField(blank=True)

    # dbs
    dbs_status = models.CharField(
        max_length=50,
        default="not_started"
    )

    # training
    training_data = models.JSONField(default=dict, blank=True)

    # banking info (need to encrypt or outsource into an external service)
    bank_account_name = models.CharField(max_length=255, blank=True)
    bank_name = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=34, blank=True)
    sort_code = models.CharField(max_length=16, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"VolunteerProfile({self.user.username})"