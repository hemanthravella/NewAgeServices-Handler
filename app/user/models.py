"""This  holds the custom models for custom user creationn"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser,PermissionsMixin):
    """Has fields needed for User creation"""

