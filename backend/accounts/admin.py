from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = tuple(list(UserAdmin.fieldsets) + [("System Role", {"fields": ("role",)}),])
    list_display = tuple(UserAdmin.list_display) + ("role",)
    list_filter = tuple(UserAdmin.list_filter) + ("role",)

# User is registered via the @admin.register(User) decorator above.
# admin.site.register(User, CustomUserAdmin)
