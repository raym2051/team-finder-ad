"""Админ-панель для пользователей"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.forms import CustomUserCreationForm

User = get_user_model()  # get_user_model вместо прямого импорта


@admin.register(User)
class UserAdminConfig(UserAdmin):
    """Кастомная админ-панель пользователя"""

    add_form = CustomUserCreationForm
    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "date_joined")
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("username", "email")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "github_url", "avatar")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
