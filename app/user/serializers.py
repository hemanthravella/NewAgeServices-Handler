"""This serializes the data and pass to User Model"""
from smtpd import usage

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """This serializes the data for creating user"""

    class Meta():
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password' : {
                'write_only' : True,
                'min_length' : 5
            }
        }

    def create(self, validated_data):
        """Created and return user with encrypted data[Excludes password from response]"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """This will be used to update the password"""
        password = validated_data.pop('password', None)
        user = super().update(instance=instance,validated_data=validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user