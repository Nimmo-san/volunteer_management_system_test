from rest_framework import serializers
from .models import VolunteerProfile


class VolunteerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerProfile
        fields = "__all__"
        # to separate private fields, like bank accounts info
        # need to create a second serializer for staff/admin
        read_only_fields = ["id", "created_at", "updated_at"]