"""This will serialize the orders"""

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """To serialize the order items of the order"""
    item_total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['item_name', 'quantity', 'item_price', 'item_total']


class GetOrderSerializer(serializers.ModelSerializer):
    """To serialize the order"""
    order_items = OrderItemSerializer(many=True) #There will be multiple order items in a order
    order_cost = serializers.SerializerMethodField()
    order_quantity = serializers.SerializerMethodField()
    order_status = serializers.CharField(source='status') #to get status from the order and send it to order_status

    class Meta:
        model = Order
        fields = ['order_id', 'order_origin', 'status', 'order_placed_ts', 'order_total', 'order_quantity', 'order_status', 'order_items']

    def get_order_cost(self, obj: Order) -> str:
        """calculate the order cost by summing all order items cost"""
        return f"${sum(item.item_total for item in obj.order_items.all()):.2f}"

    def get_order_quantity(self, obj: Order) -> int:
        """Calculate the total quantity of items in the order"""
        return sum(item.quantity for item in obj.order_items.all())

    def to_representation(self, instance: Order) -> dict:
        # Format order date as an ISO string
        representation = super().to_representation(instance)
        representation['order_date'] = instance.order_placed_ts
        representation['order_status'] = instance.get_status_display()  # Get the human-readable status
        return representation
