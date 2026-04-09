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





from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CompanyProfile

class AdminCompanyUpdateViewTest(APITestCase):
    def setUp(self):
        # Create a Superuser
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpassword"
        )
        # Create a Regular User
        self.regular_user = User.objects.create_user(
            username="driver", password="driverpassword"
        )
        
        # Create initial profile
        self.profile = CompanyProfile.objects.create(
            name="Original Name",
            hero_title="Old Title",
            contact_email="old@fuel.com"
        )
        
        self.url = reverse('company-update') # Ensure this matches your urls.py name

    def test_update_success_as_admin(self):
        """Tests that a superuser can update the profile."""
        self.client.force_authenticate(user=self.admin_user)
        data = {"hero_title": "New Smart Fuel Title"}
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.hero_title, "New Smart Fuel Title")

    def test_update_forbidden_for_regular_user(self):
        """Tests that a non-superuser cannot update the profile."""
        self.client.force_authenticate(user=self.regular_user)
        data = {"hero_title": "Hacker Title"}
        
        response = self.client.put(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.hero_title, "Old Title")

    def test_update_unauthenticated(self):
        """Tests that anonymous users are rejected."""
        response = self.client.put(self.url, {"hero_title": "No Auth"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)