from django.test import TestCase
from django.contrib.auth.models import User
from .serializers import MyTokenObtainPairSerializer

class TokenSerializerTest(TestCase):
    def setUp(self):
        # Create a test user
        self.username = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(
            username=self.username, 
            password=self.password,
            is_staff=True,
            is_superuser=False
        )

    def test_token_contains_custom_claims(self):
        """Tests if the encrypted JWT payload contains our custom fields."""
        serializer = MyTokenObtainPairSerializer()
        token = serializer.get_token(self.user)
        
        # Checking the token payload (claims)
        self.assertEqual(token['username'], self.username)
        self.assertEqual(token['is_superuser'], False)

    def test_serializer_response_data(self):
        """Tests if the JSON response body contains the extra user info."""
        data = {
            "username": self.username,
            "password": self.password
        }
        serializer = MyTokenObtainPairSerializer(data=data)
        
        # Validating the serializer triggers the validate() method
        self.assertTrue(serializer.is_valid())
        
        # Check the dictionary returned for the frontend
        response_data = serializer.validated_data
        self.assertEqual(response_data['username'], self.username)
        self.assertEqual(response_data['is_staff'], True)
        self.assertEqual(response_data['is_superuser'], False)
        
        
        
        


from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory
from .models import CompanyProfile
from .serializers import CompanyProfileSerializer

class CompanyProfileSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.logo = SimpleUploadedFile(
            name='logo.png',
            content=b'\x89PNG\r\n\x1a\n...', # Mock PNG header
            content_type='image/png'
        )
        self.company = CompanyProfile.objects.create(
            name="Smart Fuel Distro",
            hero_title="Efficiency in Every Drop",
            hero_subtitle="Optimizing fuel logistics with real-time data.",
            contact_email="contact@smartfuel.com",
            logo=self.logo
        )

    def test_serializer_output_fields(self):
        """Tests that the serializer returns the correct fields and values."""
        request = self.factory.get('/')
        serializer = CompanyProfileSerializer(instance=self.company, context={'request': request})
        data = serializer.data

        # Check that expected fields are present
        expected_fields = {'hero_title', 'hero_subtitle', 'contact_email', 'logo'}
        self.assertEqual(set(data.keys()), expected_fields)
        
        # FIX: Use assertIn to check for the directory and file extension 
        # rather than the exact filename string.
        self.assertIn('/assets/', data['logo'])
        self.assertTrue(data['logo'].endswith('.png'))

    def test_serializer_omits_name(self):
        """Tests that the 'name' field is NOT in the serialized data (as per your Meta class)."""
        serializer = CompanyProfileSerializer(instance=self.company)
        self.assertNotIn('name', serializer.data)

    def test_invalid_email_data(self):
        """Tests that the serializer catches invalid email formats."""
        invalid_data = {
            "hero_title": "Title",
            "hero_subtitle": "Subtitle",
            "contact_email": "not-an-email",
            "logo": self.logo
        }
        serializer = CompanyProfileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('contact_email', serializer.errors)
        
        
        
        


from django.test import TestCase
from .serializers import ContactInquirySerializer

class ContactInquirySerializerTest(TestCase):
    def setUp(self):
        self.valid_payload = {
            "name": "Mark Sekibaala",
            "email": "mark@example.com",
            "subject": "Fuel Delivery Inquiry",
            "message": "I would like to inquire about smart distribution costs."
        }

    def test_valid_serializer(self):
        """Tests that the serializer is valid with correct data."""
        serializer = ContactInquirySerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], self.valid_payload['name'])

    def test_invalid_email(self):
        """Tests that an incorrect email format is rejected."""
        payload = self.valid_payload.copy()
        payload['email'] = 'not-an-email'
        serializer = ContactInquirySerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_missing_required_fields(self):
        """Tests that the serializer fails if a required field is missing."""
        payload = {"name": "Mark"}  # Missing email, subject, and message
        serializer = ContactInquirySerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('subject', serializer.errors)
        self.assertIn('message', serializer.errors)

    def test_readonly_fields_omitted(self):
        """Tests that fields like 'is_resolved' are not accepted even if sent."""
        payload = self.valid_payload.copy()
        payload['is_resolved'] = True  # This field isn't in the Serializer Meta
        serializer = ContactInquirySerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        # is_resolved should NOT be in validated_data because it's not in the 'fields' list
        self.assertNotIn('is_resolved', serializer.validated_data)