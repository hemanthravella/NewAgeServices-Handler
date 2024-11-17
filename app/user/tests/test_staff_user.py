"""Tests for staff user API"""
from operator import truediv

from django.db.models import BooleanField
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_STAFF_USER_URL = reverse('user:create_staff_user')

def create_user(**params):
    """create and return the user"""
    return get_user_model().objects.create_user(**params)

def create_super_user(**params):
    """create and return the superuser"""
    return get_user_model().objects.create_superuser(**params)

class StaffSuperUserAPITests(TestCase):
    """Test the features of the create/staffUser API"""

    def setUp(self):
        self.super_user = create_super_user(
            email="superuser@example.com",
            password="testSuperUser")
        self.client = APIClient()
        self.client.force_authenticate(user=self.super_user)


    def test_create_admin_staff_user(self):
        """This is to test admin staff user creation"""
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

    def test_create_staff_staff_user(self):
        """This is to test staff user creation"""
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





