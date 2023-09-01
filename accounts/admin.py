from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm

CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "username",
        "email",
        "is_superuser",
    )

    search_fields = ["name"]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().fieldsets + (
            (
                "info",
                {
                    "fields": [
                        "age",
                    ]
                },
            ),
        )
        return fieldsets
