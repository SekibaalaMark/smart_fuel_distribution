from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CompanyProfile
from django.core.exceptions import ValidationError
class CompanyProfileModelTest(TestCase):
    def setUp(self):
        """
        Create a dummy image and a CompanyProfile instance for testing.
        """
        self.test_logo = SimpleUploadedFile(
            name='test_logo.jpg', 
            content=b'\x00\x01\x02\x03', 
            content_type='image/jpeg'
        )
        
        self.company = CompanyProfile.objects.create(
            name="Enkizo Tech",
            hero_title="Building the Future",
            hero_subtitle="We provide high-quality vocational training and digital solutions.",
            contact_email="info@enkizo.com",
            logo=self.test_logo
        )

    def test_company_profile_creation(self):
        """Tests if the model correctly saves the data."""
        self.assertEqual(self.company.name, "Enkizo Tech")
        self.assertEqual(self.company.hero_title, "Building the Future")
        self.assertEqual(self.company.contact_email, "info@enkizo.com")
        self.assertTrue(self.company.logo.name.startswith('assets/test_logo'))

    def test_str_representation(self):
        """Tests the __str__ method returns the company name."""
        self.assertEqual(str(self.company), self.company.name)

    def test_max_length_constraints(self):
        """Tests that the max_length constraints are respected."""
        # Getting the field object to check its max_length attribute
        max_length = self.company._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
    from django.core.exceptions import ValidationError

# Add this method to your CompanyProfileModelTest class
def test_invalid_email_raises_error(self):
    """Tests that an improperly formatted email raises a ValidationError."""
    self.company.contact_email = "not-an-email"
    with self.assertRaises(ValidationError):
        self.company.full_clean()