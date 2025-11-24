from rest_framework import serializers

from .models import Placement, Shift


class PlacementSerializer(serializers.ModelSerializer):
    volunteer_username = serializers.CharField(
        source="volunteer.user.username",
        read_only=True,
    )
    opportunity_title = serializers.CharField(
        source="opportunity.title",
        read_only=True,
    )

    class Meta:
        model = Placement
        fields = [
            "id",
            "volunteer",
            "volunteer_username",
            "opportunity",
            "opportunity_title",
            "supervisor",
            "start_date",
            "end_date",
            "hours_per_week",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "volunteer_username",
            "opportunity_title",
            "created_at",
            "updated_at",
        ]


class ShiftSerializer(serializers.ModelSerializer):
    placement_display = serializers.CharField(
        source="placement.__str__",
        read_only=True,
    )

    class Meta:
        model = Shift
        fields = [
            "id",
            "placement",
            "placement_display",
            "start",
            "end",
            "location",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "placement_display", "created_at", "updated_at"]
