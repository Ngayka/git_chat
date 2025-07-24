from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status

User = get_user_model()


class AccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_account(self):
        url = reverse("user:create")
        data = {'username': 'user1',
                'email': 'user1@example.com',
                'password': 'user_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class LoginTestCase(APITestCase):
    def test_login(self):
        data = {'username': 'user1',
                'password': 'secret',
                'email': 'user1@test.com'}
        response = self.client.post('/api/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

