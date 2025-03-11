from rest_framework import serializers
from .models import OrderItem, Order, Cart
from datetime import timedelta
from django.utils import timezone
from restaurant.serializers import MenuItemSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']

    def validate_items(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Items must be a dictionary.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_price'] = instance.total_price()
        return representation


class CreateOrderSerializer(serializers.Serializer):
    delivery_time = serializers.DateTimeField()
    delivery_address = serializers.CharField(max_length=255)

    def validate_delivery_time(self, value):
        if value < timezone.now() + timedelta(minutes=30):
            raise serializers.ValidationError("Delivery time must be at least 30 minutes from now")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'delivery_time', 'is_delivered',
                  'delivery_address']
