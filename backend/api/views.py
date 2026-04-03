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