from rest_framework.test import APITestCase
from rest_framework import status
from .models import MenuItem
from django.contrib.auth import get_user_model
from decimal import Decimal

class MenuItemSerializerTest(APITestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password',
        )

        self.menu_item_1 = MenuItem.objects.create(
            name='Pizza Margherita',
            description='Classic Margherita pizza with mozzarella and basil',
            price=10.99,
        )
        self.menu_item_2 = MenuItem.objects.create(
            name='Pasta Carbonara',
            description='Traditional Italian pasta carbonara',
            price=12.50,
        )

    def test_menu_item_list(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/restaurant/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_menu_item_create(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'Caesar Salad',
            'description': 'Crispy romaine lettuce with Caesar dressing and croutons',
            'price': '8.99',
        }
        response = self.client.post('/api/restaurant/menu-items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['price'], data['price'])

    def test_menu_item_update(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'Updated Pizza Margherita',
            'description': 'Updated classic Margherita pizza with mozzarella and basil',
             'price': Decimal('11.99'),
        }
        response = self.client.put(f'/api/restaurant/menu-items/{self.menu_item_1.id}/', data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item_1.refresh_from_db()
        self.assertEqual(self.menu_item_1.name, data['name'])
        self.assertEqual(self.menu_item_1.description, data['description'])
        self.assertEqual(self.menu_item_1.price, data['price'])

    def test_menu_item_delete(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/restaurant/menu-items/{self.menu_item_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MenuItem.objects.filter(id=self.menu_item_1.id).exists())

    def test_menu_item_create_invalid_data(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': '',
            'description': 'Valid description',
            'price': 'invalid_price',
        }
        response = self.client.post('/api/restaurant/menu-items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
