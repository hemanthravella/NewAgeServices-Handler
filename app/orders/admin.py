from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from . import models

class OrderAdmin(admin.ModelAdmin):  # Inherit from admin.ModelAdmin
    """Admin panel for improved Order view"""
    ordering = ('order_id',)
    list_display = ('order_id', 'customer_id', 'status', 'total_cost')

class OrderItemAdmin(admin.ModelAdmin):  # Inherit from admin.ModelAdmin
    """Admin panel for improved Order view"""
    ordering = ('order',)
    list_display = ('order', 'menu_item', 'item_total', 'quantity', 'item_name','item_price')

admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
