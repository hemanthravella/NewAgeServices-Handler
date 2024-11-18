from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from . import models

class MenuAdmin(admin.ModelAdmin):  # Inherit from admin.ModelAdmin
    """Admin panel for improved menu view"""
    ordering = ('item_name',)
    list_display = ('item_name', 'menu_type', 'is_available')

admin.site.register(models.MenuItem, MenuAdmin)
