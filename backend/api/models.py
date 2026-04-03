# models.py
from django.db import models

class CompanyProfile(models.Model):
    name = models.CharField(max_length=200)
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.TextField()
    contact_email = models.EmailField()
    logo = models.ImageField(upload_to='assets/')

    def __str__(self):
        return self.name
    
    
    


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
