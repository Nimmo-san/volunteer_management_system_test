from django.contrib import admin
from .models import Opportunity, Application, Interview


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "program", "is_active", "positions", "created_at")
    list_filter = ("is_active", "program__department")
    search_fields = ("title", "description", "program__title")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("opportunity", "volunteer", "status", "submitted_at")
    list_filter = ("status",)
    search_fields = ("opportunity__title", "volunteer__user__username")


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ("application", "scheduled_at", "interviewer", "outcome")
    list_filter = ("outcome",)
    search_fields = ("application__opportunity__title", "application__volunteer__user__username")
