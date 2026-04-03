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