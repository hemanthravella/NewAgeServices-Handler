"""This will serialize the orders"""

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Order, OrderItem
from menu.models import MenuItem


class OrderItemSerializer(serializers.ModelSerializer):
    """To serialize the order items of the order"""
    item_total = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['order', 'menu_item', 'item_name', 'quantity', 'item_price', 'item_total']


class GetOrderSerializer(serializers.ModelSerializer):
    """To serialize the order"""
    order_items = OrderItemSerializer(many=True)  # There will be multiple order items in a order
    order_cost = serializers.SerializerMethodField()
    order_quantity = serializers.SerializerMethodField()
    order_status = serializers.CharField(source='status')  # to get status from the order and send it to order_status

    class Meta:
        model = Order
        fields = ['order_id', 'order_origin', 'status', 'order_placed_ts', 'order_cost', 'order_quantity',
                  'order_status', 'order_items']

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


class CreateOrderItemSerializer(serializers.ModelSerializer):
    """To serialize the item_id and quantity for adding to the order"""

    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = ['item_id', 'quantity']

    def validate_item_id(self, value: item_id) -> int:
        """To check if the item exist with provided id"""
        if not MenuItem.objects.filter(item_id=value).exists():
            raise serializers.ValidationError(f"Menu item with ID {value} does not exist.")
        return value


class CreateOrderSerializer(serializers.ModelSerializer):
    """To serialize the create order"""
    order_items = CreateOrderItemSerializer(many=True, write_only=True)  # Accept order items in request

    class Meta:
        model = Order
        fields = ['order_origin', 'order_items']

    def create(self, validated_data):
        """Create an order with the items inside the request"""
        order_items_data = validated_data.pop('order_items')

        # create order first before adding items. as order item need order as fk
        order = Order.objects.create(**validated_data)

        # to get all menu items in one query
        menu_item_ids = [item['item_id'] for item in order_items_data]
        menu_items = {item.item_id: item for item in MenuItem.objects.filter(item_id__in=menu_item_ids)}

        for item_data in order_items_data:
            menu_item = menu_items.get(item_data['item_id'])
            if not menu_item:
                raise serializers.ValidationError(f"Menu item with ID {item_data['item_id']} does not exist.")

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                item_name=menu_item.item_name,
                quantity=item_data['quantity'],
                item_price=menu_item.item_cost
            )

        return order
