from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import AuthorityProfile, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    ordering = ["-date_joined"]
    list_display = ["email", "name", "phone", "trust_score", "is_authority", "is_active"]
    search_fields = ["email", "name", "phone"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Profile", {"fields": ("name", "phone", "area")}),
        ("Trust", {"fields": ("trust_score", "verified_reports", "false_reports")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "name", "password1", "password2")}),
    )


@admin.register(AuthorityProfile)
class AuthorityProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "department", "area"]
