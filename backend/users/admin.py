from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('avatar',)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets

    ordering = ('email',)
    search_fields = ('email', 'username')
