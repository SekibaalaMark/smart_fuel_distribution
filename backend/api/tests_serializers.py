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