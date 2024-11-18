"""This will have the serializers for MenuItems"""

from rest_framework import serializers

from .models import MenuItem


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

    def update(self, instance, validated_data, **kwargs):
        """To validate the data which is sent using patch"""
        try:
            for key, value in validated_data.items():
                if hasattr(instance,key):
                    setattr(instance,key,value)
                else: raise AttributeError(f"{key} is not a valid attribute of {type(instance).__name__}")

            for key,value in kwargs.items():
                if hasattr(instance,key):
                    setattr(instance,key,value)
                else: raise AttributeError(f"{key} is not a valid attribute of {type(instance).__name__}")

            instance.save()

        except AttributeError as ae:
            raise serializers.ValidationError(f"Invalid attribute update: {ae}")

        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred during update: {e}")

        return instance
