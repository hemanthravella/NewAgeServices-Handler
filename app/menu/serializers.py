"""This will have the serializers for MenuItems"""

from rest_framework import serializers

from .models import MenuItem, MenuAudit


class MenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ['item_create_date']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Restrict to specified fields
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, attrs):
        """This validates the fields to be part of model"""
        bad_data = set(self.initial_data.keys())-set(self.fields.keys())

        if bad_data:
            raise serializers.ValidationError(
                {field: "Bad-input." for field in bad_data}
            )

        return attrs

class MenuAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuAudit
        fields = '__all__'

