"""This contains the models related to the orders placed"""

from django.db import models
from user.models import User
from menu.models import MenuItem


class Order(models.Model):
    """Tracks customer orders"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    ORDER_ORIGIN_CHOICES = [
        ('online', 'Online'),
        ('restaurant', 'Restaurant'),
        ('table', 'Table'),
    ]
    order_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for the order."
    )
    customer_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="orders",
        help_text="Customer who placed the order."
    )
    order_placed_ts = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the order was placed."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the order placed."
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="total_cost_of_the_order"
    )
    order_last_upd_ts = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the order is last updated."
    )
    table_number = models.IntegerField(
        max_length=5,
        null=True,
        blank=True,
        help_text="Number of the table the order belongs to."
    )

    order_origin = models.CharField(
        max_length=20,
        choices=ORDER_ORIGIN_CHOICES,
        null=True,
        blank=True,
        help_text="The origin of the order"
    )

    def __str__(self):
        return self.order_id

    def set_order_origin(self, user):
        """To set the origin manually based on logged in User as it is None"""
        if user.is_staff:
            self.order_origin = 'restaurant'
        else:
            self.order_origin = 'online'

    def save(self, *args, **kwargs):
        """Override save to set the order origin when saving the order"""
        if not self.order_origin:
            # If at all order origin is empty, set it with customer first_name
            self.set_order_origin(self.customer_id.first_name)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Maps the menu items with the order id"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",  # This allows reverse access to order_items from Order
        help_text="Reference to the order."
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        help_text="Menu item in the order."
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Quantity of the order placed for the Menu item."
    ),
    item_name = models.CharField(
        max_length=50,
        help_text="Name of the menu item (max 50 characters)."
    )
    item_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Price of the Menu Item."
    )
    item_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="item price * quantity"
    )

    def save(self, *args, **kwargs):
        """To manually update the item price"""
        if not self.item_name:
            self.item_name = self.menu_item.item_name

        if not self.item_price:
            # Set item_price from the MenuItem.item_cost if not provided
            self.item_price = self.menu_item.item_cost

        if self.item_price is not None and self.quantity is not None:
            self.item_total = self.item_price * self.quantity
        else:
            self.item_total = 0.00

        super().save(*args, **kwargs)
