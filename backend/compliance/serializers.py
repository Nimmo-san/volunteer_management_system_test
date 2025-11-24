from rest_framework import serializers

from .models import ComplianceCheck


class ComplianceCheckSerializer(serializers.ModelSerializer):
    volunteer_username = serializers.CharField(
        source="volunteer.user.username",
        read_only=True,
    )

    class Meta:
        model = ComplianceCheck
        fields = [
            "id",
            "volunteer",
            "volunteer_username",
            "check_type",
            "status",
            "details",
            "expires_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "volunteer_username", "created_at", "updated_at"]
