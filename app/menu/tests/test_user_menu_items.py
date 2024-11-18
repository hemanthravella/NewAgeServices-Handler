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


class MenuItemDetailTests(TestCase):
    """Test retrieving a single menu item by item_id"""

    def setUp(self):
        # Create a test user
        self.user = create_user(email="user@example.com", password="password123")

        # Create a menu item
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
        self.menu_item = create_menu_item(**self.item_data)

        # Create an API client and authenticate the user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Define the URL for the item detail view
        self.url = reverse('menu:menu-item-detail', args=[self.menu_item.item_id])

    def test_get_menu_item_success(self):
        """Test retrieving a menu item by its item_id successfully."""
        # Make the GET request to fetch the menu item details
        response = self.client.get(self.url)

        # Assert the status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data matches the menu item data
        self.assertEqual(response.data, {
            'item_name': self.menu_item.item_name,
            'item_type': self.menu_item.item_type,
            'menu_type': self.menu_item.menu_type,
            'item_cost': str(self.menu_item.item_cost),
            'item_description': self.menu_item.item_description,
            'is_allergic': self.menu_item.is_allergic,
            'is_vegetarian': self.menu_item.is_vegetarian,
            'is_available': self.menu_item.is_available,
        })

    def test_get_menu_item_not_found(self):
        """Test retrieving a non-existent menu item by its item_id."""
        # Create a URL with a non-existent item_id (invalid ID)
        invalid_url = reverse('menu:menu-item-detail', args=[99999])

        # Make the GET request to fetch the non-existent menu item
        response = self.client.get(invalid_url)

        # Assert the status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No MenuItem matches the given query.')
