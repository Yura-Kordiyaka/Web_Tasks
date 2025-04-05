from rest_framework import status, permissions, generics
from rest_framework.response import Response
from .models import Order, OrderItem, Cart
from restaurant.models import MenuItem
from rest_framework.views import APIView
from .serializers import OrderSerializer, CartSerializer, CreateOrderSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from app.tasks import send_order_delivered_email
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrderFilter
from rest_framework.exceptions import NotAuthenticated


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get cart contents",
        description="Retrieves the current user's shopping cart and its items.",
        responses={200: CartSerializer},
    )
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(
        summary="Add items to cart",
        description="Adds items to the cart. Provide a dictionary "
                    "where keys are menu item IDs and values are quantities.",
        request={
            "application/json": {
                "example": {
                    "items": {
                        "1": 2,
                        "3": 5
                    }
                }
            }
        },
        responses={
            200: {"description": "Items added successfully", "example": {"status": "items added"}},
            400: {"description": "Validation error", "example": {"error": "Items must be a dictionary"}}
        }
    )
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = request.data.get("items", {})

        if not isinstance(items, dict):
            return Response({"error": "Items must be a dictionary"}, status=status.HTTP_400_BAD_REQUEST)

        invalid_items = []
        for menu_item_id, quantity in items.items():
            if not MenuItem.objects.filter(id=menu_item_id).exists():
                invalid_items.append(menu_item_id)
            else:
                cart.add_item(menu_item_id, quantity)

        if invalid_items:
            return Response({"error": f"Menu items not found: {invalid_items}"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "items added"}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update cart item quantities",
        description="Updates the quantities of items in the cart. If the quantity is <= 0, the item is removed.",
        request={
            "application/json": {
                "example": {
                    "items": {
                        "1": 3,
                        "2": 0
                    }
                }
            }
        },
        responses={
            200: {"description": "Cart updated successfully", "example": {"status": "cart updated"}},
            400: {"description": "Validation error", "example": {"error": "Items must be a dictionary"}}
        }
    )
    def put(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = request.data.get("items", {})

        if not isinstance(items, dict):
            return Response({"error": "Items must be a dictionary"}, status=status.HTTP_400_BAD_REQUEST)

        for menu_item_id, quantity in items.items():
            if quantity <= 0:
                cart.remove_item(menu_item_id)
            else:
                cart.update_item_quantity(menu_item_id, quantity)

        return Response({"status": "cart updated"}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Remove items from cart",
        description="Removes specified items from the cart.",
        request={
            "application/json": {
                "example": {
                    "items": [1, 2, 3]
                }
            }
        },
        responses={
            200: {"description": "Items removed successfully", "example": {"status": "items removed"}},
            400: {"description": "Validation error", "example": {"error": "Items must be a list"}}
        }
    )
    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = request.data.get("items", [])

        if not isinstance(items, list):
            return Response({"error": "Items must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        cart.items.clear()
        cart.save()

        return Response({"status": "items removed"}, status=status.HTTP_200_OK)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create order",
        request=CreateOrderSerializer,
        responses={201: OrderSerializer, 400: {"error": "Cart is empty"}}
    )
    def post(self, request):
        """Create an order from the cart"""
        cart, _ = Cart.objects.get_or_create(user=request.user)

        if not cart.items:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        delivery_time = serializer.validated_data['delivery_time']
        delivery_address = serializer.validated_data['delivery_address']
        order = Order.objects.create(user=request.user, delivery_time=delivery_time, delivery_address=delivery_address,
                                     total_price=cart.total_price())

        for menu_item_id, quantity in cart.items.items():
            menu_item = MenuItem.objects.get(id=menu_item_id)
            OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)
        if timezone.is_naive(delivery_time):
            eta = timezone.make_aware(delivery_time)
        else:
            eta = delivery_time
        send_order_delivered_email.apply_async(
            args=[request.user.email, request.user.first_name, order.id],
            eta=eta
        )
        cart.items.clear()
        cart.save()

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("User is not authenticated")

        return Order.objects.filter(user=user)

class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'
