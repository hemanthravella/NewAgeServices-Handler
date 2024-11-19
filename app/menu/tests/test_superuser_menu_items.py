"""SUPER USER ACCESS : Tests for the menu API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from menu.models import MenuItem,MenuAudit


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

class SuperUserMenuCreatePermissionAPITests(TestCase):
    """Test the menu creation by superuser access"""

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
        self.superuser = create_super_user(
            email="superuser@example.com",
            password="testSuperUser")
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)

    def test_superuser_create_menu_item(self):
        """this is to test superuser creating menu item"""

        res = self.client.post(CREATE_MENU_URL, self.item)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['item_name'],self.item['item_name'])

class SuperUserUpdateMenuItemAPI(TestCase):
    """This is to test if the Super user can update the menu item using menu-item-patch"""

    def setUp(self):
        # Create a test user
        self.user = create_super_user(email="Superuser1@example.com", password="password123")

    def test_Super_user_update_menu_item_Success(self):
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
        self.assertEqual(self.user.email, self.get_res.data['item_upd_usr_email'])

    def test_super_user_updating_item_not_found(self):
        """To test superuser update item which is not available"""
        self.item_patch_data = {
            "item_name": "Updated Samosa",
            "item_type": "Snacking"
        }

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.patch_url = reverse('menu:menu-item-patch', kwargs={'item_id':9999})
        self.patch_res = self.client.patch(self.patch_url, data=self.item_patch_data)

        self.assertEqual(self.patch_res.status_code,status.HTTP_404_NOT_FOUND)


class SuperUserDeleteMenuItemAPI(TestCase):

    def setUp(self):
        # Create a test user
        self.user = create_super_user(email="user@example.com", password="password123")

    def test_superuser_delete_menu_item_success(self):
        """To test if the superuser access can delete the menu item"""
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
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.del_url = reverse('menu:menu-item-delete', kwargs={'item_id':self.menu_item.item_id})
        self.res = self.client.delete(self.del_url)
        self.assertEqual(self.res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.res.data['deleted_by_usr_email'], self.user.email)
        self.assertEqual(self.res.data['item_id'], self.menu_item.item_id)
        self.assertEqual(self.res.data['item_name'], self.menu_item.item_name)

        self.menu_audit_item = MenuAudit.objects.get(id=self.res.data['id'])
        self.assertEqual(self.menu_audit_item.deleted_by_usr_email,self.user.email)
        self.assertEqual(self.menu_audit_item.item_name,self.item_data['item_name'])
        self.assertEqual(self.menu_audit_item.item_id,self.menu_item.item_id)

        with self.assertRaises(MenuItem.DoesNotExist):
            MenuItem.objects.get(item_id=self.menu_item.item_id)
