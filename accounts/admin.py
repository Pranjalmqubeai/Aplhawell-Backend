# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Admin 'Add user' form that uses email as the identifier."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "role")

    def save(self, commit=True):
        user = super().save(commit=False)
        # If you still keep username field on the model for compatibility,
        # set a sensible default so it's never empty.
        if hasattr(user, "username") and not user.username:
            user.username = (user.email or "").split("@")[0]
        if commit:
            user.save()
            self.save_m2m()
        return user


class CustomUserChangeForm(UserChangeForm):
    """Admin 'Change user' form."""
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name", "role",
                  "is_active", "is_staff", "is_superuser", "groups", "user_permissions")


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Email-first user admin with role support."""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    # What you see in the list page
    list_display = ("email", "role", "is_active", "is_staff", "is_superuser", "date_joined", "last_login")
    list_filter = ("role", "is_active", "is_staff", "is_superuser", "groups")
    ordering = ("-date_joined",)
    search_fields = ("email", "first_name", "last_name")

    # Make important dates read-only
    readonly_fields = ("date_joined", "last_login")

    # Hide username entirely from the admin forms (we authenticate by email)
    # NOTE: We do NOT include 'username' in any fieldset below.
    fieldsets = (
        (_("Credentials"), {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Role"), {"fields": ("role",)}),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Fields used when creating a new user from admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "role",
                "password1",
                "password2",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
            ),
        }),
    )
