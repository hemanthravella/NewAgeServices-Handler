"""This will have the serializers for MenuItems"""

from rest_framework import serializers

from .models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ['item_create_date']
