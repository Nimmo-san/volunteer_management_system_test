from django.contrib import admin
from .models import ComplianceCheck


@admin.register(ComplianceCheck)
class ComplianceCheckAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "check_type", "status", "expires_at", "updated_at")
    list_filter = ("check_type", "status")
    search_fields = ("volunteer__user__username", "volunteer__user__email")
