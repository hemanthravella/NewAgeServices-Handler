"""Tests for staff user API"""
from operator import truediv

from django.db.models import BooleanField
from django.template.defaultfilters import first
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_STAFF_USER_URL = reverse('user:create_staff_user')
ME_URL = reverse('user:me')

def create_user(**params):
    """create and return the user"""
    return get_user_model().objects.create_user(**params)

def create_super_user(**params):
    """create and return the superuser"""
    return get_user_model().objects.create_superuser(**params)

def create_admin_user(**params):
    user = create_user(**params)
    user.is_admin = True
    user.save()
    return user

def create_staff_user(**params):
    user = create_user(**params)
    user.is_staff = True
    user.save()
    return user

class StaffSuperUserAPITests(TestCase):
    """Test the features of the create/staffUser API"""

    def setUp(self):
        self.super_user = create_super_user(
            email="superuser@example.com",
            password="testSuperUser")
        self.client = APIClient()
        self.client.force_authenticate(user=self.super_user)


    def test_superuser_create_admin_user(self):
        """This is to test admin staff user creation by superuser"""
        payload = {
            'email': "testadmin@example.com",
            'password': 'testpassword',
            'first_name': 'admin',
            'last_name': 'user',
            'is_admin': True,
            'is_staff': True,
            'is_superuser': False
        }
        res = self.client.post(CREATE_STAFF_USER_URL,payload)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

        self.client.force_authenticate(user=user)
        me_res = self.client.get(ME_URL)
        self.assertEqual(me_res.status_code, status.HTTP_200_OK)
        self.assertEqual(me_res.data, {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_admin': user.is_admin,
            'is_superuser': user.is_superuser,
        })

    def test_superuser_create_staff_user(self):
        """This is to test staff user creation by superuser"""
        payload = {
            'email': "testadmin@example.com",
            'password': 'testpassword',
            'first_name': 'admin',
            'last_name': 'user',
            'is_admin': False,
            'is_staff': True,
            'is_superuser': False
        }
        res = self.client.post(CREATE_STAFF_USER_URL,payload)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

        self.client.force_authenticate(user=user)
        me_res = self.client.get(ME_URL)
        self.assertEqual(me_res.status_code,status.HTTP_200_OK)
        self.assertEqual(me_res.data,{
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_admin': user.is_admin,
            'is_superuser': user.is_superuser,
        })



class StaffAdminUserAPITests(TestCase):
    """This tests the Admin user for Staff User API"""
    def setUp(self):
        self.admin_user = create_admin_user(
            email="adminuser@example.com",
            password="testAdminUser",
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

    def test_admin_user_create_admin_staff_user(self):
        """This is to test admin staff user creation by Admin user"""
        payload = {
            'email': "testadmin@example.com",
            'password': 'testpassword',
            'first_name': 'admin',
            'last_name': 'user',
            'is_admin': True,
            'is_staff': True,
            'is_superuser': False
        }
        res = self.client.post(CREATE_STAFF_USER_URL,payload)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

        self.client.force_authenticate(user=user)
        me_res = self.client.get(ME_URL)
        self.assertEqual(me_res.status_code, status.HTTP_200_OK)
        self.assertEqual(me_res.data, {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_admin': user.is_admin,
            'is_superuser': user.is_superuser,
        })

    def test_admin_user_create_staff_staff_user(self):
        """This is to test staff user creation Admin user"""
        payload = {
            'email': "testadmin@example.com",
            'password': 'testpassword',
            'first_name': 'admin',
            'last_name': 'user',
            'is_admin': False,
            'is_staff': True,
            'is_superuser': False
        }
        res = self.client.post(CREATE_STAFF_USER_URL,payload)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

        self.client.force_authenticate(user=user)
        me_res = self.client.get(ME_URL)
        self.assertEqual(me_res.status_code,status.HTTP_200_OK)
        self.assertEqual(me_res.data,{
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_admin': user.is_admin,
            'is_superuser': user.is_superuser,
        })






