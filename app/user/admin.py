from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from user import models


class UserAdmin(BaseUserAdmin):
    """Admin panel for Improved User view"""
    ordering = ('email',)

    list_display = ('email', 'first_name', 'last_name', 'is_staff','is_admin','is_superuser','date_joined')
    search_fields = ('first_name', 'last_name', 'email')

    fieldsets = (
        (None,
         {'fields': ('username', 'password'),
          'description': "User login credentials",
          'classes': ('wide',),
          }),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(models.User,UserAdmin)
