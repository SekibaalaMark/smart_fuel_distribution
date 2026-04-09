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
        
        
        
        

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ContactInquiry

class AdminInquiryListViewTest(APITestCase):
    def setUp(self):
        # Create Users
        self.admin_user = User.objects.create_superuser(
            username="admin_mark", password="adminpassword"
        )
        self.regular_user = User.objects.create_user(
            username="driver_user", password="driverpassword"
        )
        
        # Create multiple inquiries to test ordering
        ContactInquiry.objects.create(
            name="User 1", email="u1@test.com", subject="First", message="Oldest"
        )
        ContactInquiry.objects.create(
            name="User 2", email="u2@test.com", subject="Second", message="Newest"
        )
        
        self.url = reverse('inquiry-list') # Ensure this matches your urls.py 'name'

    def test_list_inquiries_as_admin(self):
        """Tests that a superuser can see all inquiries in descending order."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Verify ordering: The first item in the list should be the most recent one (User 2)
        self.assertEqual(response.data[0]['name'], "User 2")

    def test_list_inquiries_forbidden_for_regular_user(self):
        """Tests that a regular user is blocked from seeing the inquiry list."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_inquiries_unauthenticated(self):
        """Tests that anonymous users cannot access the list."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
        
        



from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ContactInquiry

class AdminReplyEmailViewTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin_mark", password="adminpassword"
        )
        self.inquiry = ContactInquiry.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Late Delivery",
            message="My fuel delivery is 2 hours late."
        )
        # Assuming your URL pattern looks like 'admin-reply' with a <int:pk>
        self.url = reverse('admin-reply', kwargs={'pk': self.inquiry.pk})

    def test_send_reply_success(self):
        """Tests that an admin can reply, an email is sent, and the DB is updated."""
        self.client.force_authenticate(user=self.admin_user)
        reply_message = "We apologize for the delay, the truck is 5 minutes away."
        
        response = self.client.post(self.url, {"message": reply_message}, format='json')

        # 1. Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Email sent to client's inbox!")

        # 2. Check the Email Outbox
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Re: Late Delivery")
        self.assertEqual(mail.outbox[0].body, reply_message)
        self.assertEqual(mail.outbox[0].to, ["john@example.com"])

        # 3. Check DB Persistence
        self.inquiry.refresh_from_db()
        self.assertTrue(self.inquiry.is_resolved)
        self.assertEqual(self.inquiry.admin_reply, reply_message)

    def test_send_reply_empty_message(self):
        """Tests that sending an empty message returns a 400 error."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.url, {"message": ""}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Message body is empty")

    def test_inquiry_not_found(self):
        """Tests that replying to a non-existent ID returns a 404."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-reply', kwargs={'pk': 9999})
        response = self.client.post(url, {"message": "Hello"}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)