from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "street"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "street", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "street", "zip", "city", "telephone")}),
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


admin.site.register(CustomUser, CustomUserAdmin)
