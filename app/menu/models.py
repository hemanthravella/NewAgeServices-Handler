"""This contains the models related to the menu items"""

from django.db import models
from user.models import User
from django.utils.timezone import now

class MenuItem(models.Model):

    item_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for the menu item."
    )
    item_name = models.CharField(
        max_length=50,
        help_text="Name of the menu item (max 50 characters)."
    )
    item_type = models.CharField(
        max_length=50,
        help_text="Type or category of the menu item (e.g., 'Drink', 'Main Course')."
    )
    menu_type = models.CharField(
        max_length=50,
        help_text="Type or category of the menu item (e.g., 'BreakFast','Lunch','Full day')."
    )
    item_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Cost of the item in the format XX.XX (e.g., 12.50)."
    )
    item_description = models.CharField(
        max_length=255,
        help_text="Brief description of the menu item (max 255 characters)."
    )
    is_allergic = models.BooleanField(
        default=False,
        help_text="Indicates if the item contains allergens (True/False)."
    )
    is_vegetarian = models.BooleanField(
        default=False,
        help_text="Indicates if the item is vegetarian (True/False)."
    )
    item_last_upd_ts = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the last update (auto-updated)."
    )
    item_upd_usr_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,  # Prevent deletion of referenced user
        null=True,
        blank=True,
        related_name='updated_items',
        help_text="ID of the user who last updated the item."
    )
    item_upd_usr_email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Email of the user who created the item."
    )
    item_create_date = models.DateField(
        auto_now_add=True,
        help_text="Date when the item was created (auto-generated)."
    )
    is_available = models.BooleanField(
        default=True,
        help_text="This will be True/False based on availability of item"
    )


    def __str__(self):
        return self.item_name

class MenuAudit(models.Model):
    """Model to log deleted menu items."""
    id = models.AutoField(primary_key=True)
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=50)
    deleted_at = models.DateTimeField(default=now)
    deleted_by_usr_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="The user who deleted the item."
    )
    deleted_by_usr_email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Email of the user who created the item."
    )

    class Meta:
        verbose_name = "Menu Audit"
        verbose_name_plural = "Menu Audits"

    def __str__(self):
        return f"Audit Log for Item {self.item_id}: {self.item_name}"

