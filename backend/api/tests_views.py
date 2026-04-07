from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class TokenViewTest(APITestCase):
    def setUp(self):
        self.username = "mark_developer"
        self.password = "securepassword123"
        self.user = User.objects.create_user(
            username=self.username, 
            password=self.password,
            is_staff=True
        )
        # The URL name defined in your urls.py (usually 'token_obtain_pair')
        self.url = reverse('token_obtain_pair') 

    def test_login_success(self):
        """Tests that valid credentials return tokens and custom user data."""
        data = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(self.url, data, format='json')

        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for standard JWT keys
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Check for your CUSTOM data added in the Serializer's validate method
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['is_staff'], True)
        self.assertEqual(response.data['is_superuser'], False)

    def test_login_invalid_credentials(self):
        """Tests that wrong password returns 401 Unauthorized."""
        data = {
            "username": self.username,
            "password": "wrongpassword"
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)