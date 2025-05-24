from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_editable = ("step",)
    list_display_links = ("id", "user_id")
    list_filter = ("is_staff", "is_send_ads")
    list_display = (
        "id",
        "user_id",
        "step"
    )
    search_fields = ("first_name", "username", "user_id")
    ordering = ("id", )
    fieldsets = (
        (None, {"fields": ("password", "user_id")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "step",
                    "is_send_ads"
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
