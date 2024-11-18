"""ADMIN ACCESS : Tests for the menu API"""

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

class AdminMenuCreatePermissionAPITests(TestCase):
    """Test the menu creation by Admin user types"""

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
        self.adminUser = create_admin_user(
            email="adminuser@example.com",
            password="testAdminUser")
        self.client = APIClient()
        self.client.force_authenticate(user=self.adminUser)

    def test_adminUser_create_menu_item(self):
        """this is to test admin user creating menu item"""

        res = self.client.post(CREATE_MENU_URL, self.item)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['item_name'],self.item['item_name'])

class AdminUserUpdateMenuItemAPI(TestCase):
    """This is to test if the user can update the menu item using menu-item-patch"""

    def setUp(self):
        # Create a test user
        self.user = create_admin_user(email="adminuser1@example.com", password="password123")

    def test_admin_user_update_menu_item_Success(self):
        self.item_data = {
            "item_name": "Samosa",
            "item_type": "Snack",
            "menu_type": "FullDay",
            "item_cost": "1.95",
            "item_description": "Crispy and delicious snack.",
            "is_allergic": True,
            "is_vegetarian": True,
            "is_available": True
        }
        self.item_patch_data = {
            "item_name": "Updated Samosa",
            "item_type": "Snacking"
        }
        self.menu_item = create_menu_item(**self.item_data)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.patch_url = reverse('menu:menu-item-patch', kwargs={'item_id':self.menu_item.item_id})
        self.patch_res = self.client.patch(self.patch_url, data=self.item_patch_data)
        self.assertEqual(self.patch_res.status_code,status.HTTP_200_OK)

        self.get_url = reverse('menu:menu-item-detail', args=[self.menu_item.item_id])
        self.get_res = self.client.get(self.get_url)
        self.assertEqual(
            self.get_res.data["item_name"],
            self.item_patch_data["item_name"]
        )
        self.assertEqual(
            self.get_res.data["item_type"],
            self.item_patch_data["item_type"]
        )
