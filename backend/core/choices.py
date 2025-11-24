from django.db import models


class SystemRole(models.TextChoices):
    SYS_ADMIN = "SYS_ADMIN", "System Admin"
    MANAGER = "MANAGER", "Manager"
    STAFF = "STAFF", "Staff"
    VOLUNTEER = "VOLUNTEER", "Volunteer"


class ApplicationStatus(models.TextChoices):
    NEW = "NEW", "New"
    UNDER_REVIEW = "UNDER_REVIEW", "Under review"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"


class CheckType(models.TextChoices):
    DBS = "DBS", "DBS"
    REFERENCES = "REFERENCES", "References"
    RIGHT_TO_WORK = "RIGHT_TO_WORK", "Right to work"
    TRAINING = "TRAINING", "Training"
    OCC_HEALTH = "OCC_HEALTH", "Occupational health"


class CheckStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PASSED = "PASSED", "Passed"
    FAILED = "FAILED", "Failed"


class ShiftStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED", "Scheduled"
    ATTENDED = "ATTENDED", "Attended"
    MISSED = "MISSED", "Missed"
    CANCELLED = "CANCELLED", "Cancelled"