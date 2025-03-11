from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import MenuItem, Cart, Order
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

class CartViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.menu_item = MenuItem.objects.create(
            name='Test Pizza', description='Delicious pizza', price=Decimal('10.99'))
        self.cart = Cart.objects.create(user=self.user)

    def test_get_cart(self):
        self.cart.add_item(self.menu_item.id, 2)
        self.cart.save()

        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_price', response.data)
        self.assertEqual(response.data['total_price'], Decimal(self.menu_item.price * 2))

    def test_add_items_to_cart(self):
        data = {'items': {str(self.menu_item.id): 3}}
        response = self.client.post('/api/cart/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items[str(self.menu_item.id)], 3)

    def test_update_cart(self):
        self.cart.add_item(self.menu_item.id, 1)
        self.cart.save()
        data = {'items': {str(self.menu_item.id): 5}}
        response = self.client.put('/api/cart/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.items[str(self.menu_item.id)], 5)

    def test_remove_items_from_cart(self):
        self.cart.add_item(self.menu_item.id, 1)
        self.cart.save()
        data = {'items': [self.menu_item.id]}
        response = self.client.delete('/api/cart/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart.refresh_from_db()
        self.assertNotIn(str(self.menu_item.id), self.cart.items)


class OrderViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.menu_item = MenuItem.objects.create(
            name='Test Pizza', description='Delicious pizza', price=Decimal('10.99'))
        self.cart = Cart.objects.create(user=self.user)

    def test_create_order(self):
        self.cart.add_item(self.menu_item.id, 2)
        self.cart.save()

        data = {
            'delivery_time': timezone.now() + timedelta(hours=1),
            'delivery_address': 'Test Address',
        }
        response = self.client.post('/api/order/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order_data = response.data
        self.assertEqual(order_data['user'], self.user.id)
        self.assertEqual(order_data['delivery_address'], data['delivery_address'])
        self.assertEqual(order_data['total_price'], str(self.menu_item.price * 2))

    def test_create_order_empty_cart(self):
        data = {
            'delivery_time': timezone.now() + timedelta(hours=1),
            'delivery_address': 'Test Address',
        }
        response = self.client.post('/api/order/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Cart is empty')

class OrderListViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.menu_item = MenuItem.objects.create(
            name='Test Pizza', description='Delicious pizza', price=Decimal('10.99'))
        self.cart = Cart.objects.create(user=self.user)
        self.cart.add_item(self.menu_item.id, 2)
        self.cart.save()

    def test_get_orders(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'delivery_time': timezone.now() + timedelta(hours=1),
            'delivery_address': 'Test Address',
        }
        self.client.post('/api/order/', data, format='json')

        response = self.client.get('/api/order/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_orders_without_authentication(self):
        self.client.credentials()
        response = self.client.get('/api/order/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderDetailViewTests(APITestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.menu_item = MenuItem.objects.create(
            name='Test Pizza', description='Delicious pizza', price=Decimal('10.99'))
        self.cart = Cart.objects.create(user=self.user)
        self.cart.add_item(self.menu_item.id, 2)
        self.cart.save()

        self.order_data = {
            'delivery_time': timezone.now() + timedelta(hours=1),
            'delivery_address': 'Test Address',
        }

    def test_get_order_detail(self):
        self.client.force_authenticate(user=self.user)
        order_response = self.client.post('/api/order/', self.order_data, format='json')
        order_id = order_response.data['id']

        response = self.client.get(f'/api/order/{order_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], order_id)

    def test_get_order_detail_without_authentication(self):
        self.client.force_authenticate(user=self.user)
        order_response = self.client.post('/api/order/', self.order_data, format='json')
        order_id = order_response.data['id']

        self.client.logout()
        response = self.client.get(f'/api/order/{order_id}/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)