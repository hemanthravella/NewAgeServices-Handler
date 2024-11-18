"""USER ACCESS : Tests for the menu API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from menu.models import MenuItem

CREATE_MENU_URL = reverse('menu:menu-item-create')

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

def create_menu_item(**params):
    """Helper function to create and return a menu item"""
    return MenuItem.objects.create(**params)

class StaffUserMenuCreatePermissionAPITests(TestCase):
    """Test the menu creation by user access"""

    def setUp(self):

        self.item = {
                "item_name": "Samosa",
                "item_type": "Snack",
                "menu_type": "FullDay",
                "item_cost": "1.95",
                "item_description": "Samosas are triangular in shape, but can also be folded into a cone or crescent. They are typically crispy on the outside and filled with a hot and soft savory mixture.",
                "is_allergic": True,
                "is_vegetarian": True,
                "is_available": True
        }
        self.user = create_user(
            email="staffuser@example.com",
            password="testStaffUser")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_create_menu_item(self):
        """This is to test user creating menu item"""

        res = self.client.post(CREATE_MENU_URL, self.item)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_menu_item_detail_no_all(self):
        """This is to test the detail view of the item"""
        # new_item = create_menu_item(user=self.user,**self.item)
        # url = reverse('menu:menu-item-detail', args=[new_item.item_id])
        # get_res = self.client.get(url)
        #
        # self.assertEqual(get_res.status_code,status.HTTP_200_OK)
        # self.assertEqual(get_res.data, {
        #     'item_name':new_item.item_name,
        #     'is_allergic': new_item.is_allergic,
        #     'is_vegetarian': new_item.is_vegetarian,
        #     'is_available': new_item.is_available,
        #     'item_cost': new_item.item_cost
        # })
        # TODO
        pass

    def test_user_menu_item_detail_all(self):
        """This is to test the detail view of the item"""
        # new_item = create_menu_item(user=self.user,**self.item)
        # url = reverse('menu:menu-item-detail', args=[new_item.item_id])
        # get_res = self.client.get(url)
        #
        # self.assertEqual(get_res.status_code,status.HTTP_200_OK)
        # self.assertEqual(get_res.data, {
        #     'item_name':new_item.item_name,
        #     'is_allergic': new_item.is_allergic,
        #     'is_vegetarian': new_item.is_vegetarian,
        #     'is_available': new_item.is_available,
        #     'item_cost': new_item.item_cost
        # })
        # TODO
        pass