from django.contrib import admin
from authx.models import CustomUser, BlackListToken


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "role", "is_active"]
    list_filter = ["role", "is_active"]
    search_fields = ["username", "email"]


@admin.register(BlackListToken)
class BlackListTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "blacklisted_at", "reason"]
    list_filter = ["blacklisted_at", "reason"]
    search_fields = ["user__username", "user__email", "token"]
    readonly_fields = ["token", "user", "blacklisted_at"]
