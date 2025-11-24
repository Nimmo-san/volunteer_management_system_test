from django.contrib import admin
from .models import StaffProfile, ProgramRequest


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "job_title", "phone")
    search_fields = ("user__username", "user__email", "department")


@admin.register(ProgramRequest)
class ProgramRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "status", "volunteers_needed", "created_at")
    list_filter = ("status", "department")
    search_fields = ("title", "description", "department")
    autocomplete_fields = ("created_by", "primary_contact", "secondary_contacts")