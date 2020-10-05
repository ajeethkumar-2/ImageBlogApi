from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'last_login', 'is_verified')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_verified', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_verified', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)
