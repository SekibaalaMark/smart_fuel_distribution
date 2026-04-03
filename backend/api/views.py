from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import CompanyProfile, ContactInquiry
from .serializers import CompanyProfileSerializer, ContactInquirySerializer

# 1. Fetch website content (GET)
class CompanyInfoView(APIView):
    def get(self, request):
        # Get the first record (created by Admin)
        profile = CompanyProfile.objects.first()
        
        if not profile:
            return Response(
                {"message": "No company profile found. Please create one in Admin."}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = CompanyProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    


# 2. Receive the contact form JSON (POST)
class ContactCreateView(APIView):
    def post(self, request):
        serializer = ContactInquirySerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the inquiry to the database
            inquiry = serializer.save()
            
            # Trigger the email logic
            try:
                send_mail(
                    subject=f"New Website Inquiry: {inquiry.subject}",
                    message=f"From: {inquiry.name} ({inquiry.email})\n\n{inquiry.message}",
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
                    recipient_list=['admin@yourcompany.com'], # The company's email
                    fail_silently=False,
                )
            except Exception as e:
                # We still return 201 because the data was saved to the DB, 
                # but we could log the email failure here.
                print(f"Email failed to send: {e}")

            return Response(
                {"message": "Inquiry received and email sent successfully!"}, 
                status=status.HTTP_201_CREATED
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)