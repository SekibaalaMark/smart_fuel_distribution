from rest_framework import serializers
from .models import ContactInquiry, CompanyProfile

class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['hero_title', 'hero_subtitle', 'contact_email', 'logo']
        
        
        
        