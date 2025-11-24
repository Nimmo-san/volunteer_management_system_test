from django.contrib import admin
from .models import Placement, Shift


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "opportunity", "supervisor", "start_date", "end_date", "is_active")
    list_filter = ("is_active", "start_date")
    search_fields = ("volunteer__user__username", "opportunity__title")


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("placement", "start", "end", "location", "status")
    list_filter = ("status", "location")
    search_fields = ("placement__volunteer__user__username", "placement__opportunity__title")
