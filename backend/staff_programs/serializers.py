from rest_framework import serializers
from .models import StaffProfile, ProgramRequest


class StaffProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    full_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )

    class Meta:
        model = StaffProfile
        fields = [
            "id",
            "user_id",
            "username",
            "full_name",
            "department",
            "job_title",
            "phone",
        ]
        read_only_fields = ["id", "user_id", "username", "full_name"]


class ProgramRequestSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    # use IDs for contacts to keep it simple
    primary_contact = serializers.PrimaryKeyRelatedField(
        queryset=StaffProfile.objects.all(),
    )
    secondary_contacts = serializers.PrimaryKeyRelatedField(
        queryset=StaffProfile.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = ProgramRequest
        fields = [
            "id",
            "title",
            "description",
            "department",
            "volunteers_needed",
            "eligibility_status",
            "status",
            "approval_date",
            "created_by",
            "primary_contact",
            "secondary_contacts",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
