from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


class UserListViewTest(APITestCase):

    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password',
        )
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password',
        )

    def test_user_list_view_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_user_list_view_non_admin_access(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserCreateViewTest(APITestCase):

    def test_user_create_view(self):
        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "+380991234567",
            "password": "password123"
        }
        response = self.client.post('/api/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertNotIn('password', response.data)

    def test_user_create_invalid_phone_number(self):
        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "12345",
            "password": "password123"
        }
        response = self.client.post('/api/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)

class UserUpdateViewTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password',
            first_name="Old",
            last_name="Name",
            phone_number='+380991234567'
        )

    def test_user_update_view(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "first_name": "Updated",
            "last_name": "Name",
            "phone_number": "+380992345678"
        }
        response = self.client.put('/api/user/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, data['first_name'])
        self.assertEqual(self.user.last_name, data['last_name'])
        self.assertEqual(self.user.phone_number, data['phone_number'])

    def test_user_update_view_unauthenticated(self):
        data = {
            "first_name": "Updated",
            "last_name": "Name",
            "phone_number": "+380992345678"
        }
        response = self.client.put('/api/user/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)