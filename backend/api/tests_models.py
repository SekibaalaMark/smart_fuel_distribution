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
        
        


from django.test import TestCase
from .models import ContactInquiry

class ContactInquiryModelTest(TestCase):
    def setUp(self):
        self.inquiry = ContactInquiry.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            subject="Inquiry about Fuel Rates",
            message="Hello, I would like to know the current bulk fuel rates."
        )

    def test_inquiry_creation(self):
        """Tests that the inquiry is saved correctly with default values."""
        self.assertEqual(self.inquiry.name, "John Doe")
        # Check that is_resolved defaults to False
        self.assertFalse(self.inquiry.is_resolved)
        # Check that admin_reply is empty by default
        self.assertIsNone(self.inquiry.admin_reply)

    def test_created_at_auto_filled(self):
        """Tests that the created_at field is automatically populated."""
        self.assertIsNotNone(self.inquiry.created_at)

    def test_str_representation(self):
        """Tests that the string representation is the name of the inquirer."""
        # Note: If you haven't defined a __str__ method in your model yet, 
        # this test will fail. It's good practice to add one!
        self.assertEqual(str(self.inquiry), "John Doe")

    def test_resolve_inquiry(self):
        """Tests updating the inquiry status and adding a reply."""
        self.inquiry.is_resolved = True
        self.inquiry.admin_reply = "We have sent the rates to your email."
        self.inquiry.save()
        
        updated_inquiry = ContactInquiry.objects.get(id=self.inquiry.id)
        self.assertTrue(updated_inquiry.is_resolved)
        self.assertEqual(updated_inquiry.admin_reply, "We have sent the rates to your email.")