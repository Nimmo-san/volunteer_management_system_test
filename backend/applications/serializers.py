from rest_framework import serializers

from core.choices import ApplicationStatus
from .models import Opportunity, Application, Interview


class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = [
            "id",
            "program",
            "title",
            "description",
            "is_active",
            "positions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ApplicationSerializer(serializers.ModelSerializer):
    # Derive some info for convenience
    volunteer_id = serializers.IntegerField(source="volunteer.id", read_only=True)
    volunteer_username = serializers.CharField(
        source="volunteer.user.username",
        read_only=True,
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "volunteer",
            "volunteer_id",
            "volunteer_username",
            "opportunity",
            "status",
            "submitted_at",
            "updated_at",
            "notes",
        ]
        read_only_fields = [
            "id",
            "volunteer",
            "volunteer_id",
            "volunteer_username",
            # "status",  # volunteers can't set this directly, but managers/staff need to
            "submitted_at",
            "updated_at",
        ]


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = [
            "id",
            "application",
            "scheduled_at",
            "interviewer",
            "outcome",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
