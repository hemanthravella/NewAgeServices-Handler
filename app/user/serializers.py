"""This serializes the data and pass to User Model"""

from django.contrib.auth import get_user_model, authenticate
from django.template.context_processors import request
from rest_framework import serializers
from django.utils.translation import gettext as _


class UserSerializer(serializers.ModelSerializer):
    """This serializes the data for creating user"""

    class Meta():
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name',]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """Created and return user with encrypted data[Excludes password from response]"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """This will be used to update the password"""
        password = validated_data.pop('password', None)
        user = super().update(instance=instance, validated_data=validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class StaffUserSerializer(serializers.ModelSerializer):
    """This serializes the data for creating user"""

    class Meta():
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name','is_admin','is_staff','is_superuser']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """Created and return user with encrypted data[Excludes password from response]"""
        user = get_user_model().objects.create_user(**validated_data)
        user.is_staff = True
        user.is_superuser = False
        if validated_data.get('is_admin'):
            user.is_admin = True

        user.save()
        return user


    def update(self, instance, validated_data):
        """This will be used to update the password"""
        password = validated_data.pop('password', None)
        user = super().update(instance=instance, validated_data=validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class TokenAuthSerializer(serializers.Serializer):
    """Validate user and return the token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        user = authenticate(request=self.context.get('request'),username=email, password=password)

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg,code='authorization')

        attrs['user'] = user

        return attrs
