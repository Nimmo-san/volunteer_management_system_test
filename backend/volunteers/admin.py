from django.contrib import admin
from .models import VolunteerProfile


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "dbs_status", "created_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("dbs_status",)
