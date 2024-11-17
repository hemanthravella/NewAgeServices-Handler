"""This  holds the custom models for custom user creationn"""
from django.utils import timezone

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password, **extra_fields):
        """To create user"""

        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(email=email,
                          date_joined=now, **extra_fields)
        password = user.set_password(password.strip())

        user.save(using=self._db)
        return user

    def create_superuser(self,email, password,**extra_fields):
        """To Create SuperUser"""
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        user = self.create_user(email=email,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True

        user.save()
        return user


class User(AbstractBaseUser,PermissionsMixin):
    """Has fields needed for User creation"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"


