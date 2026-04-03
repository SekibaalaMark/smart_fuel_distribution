# admin.py
from django.contrib import admin
from .models import CompanyProfile, ContactInquiry

admin.site.register(CompanyProfile)
admin.site.register(ContactInquiry)