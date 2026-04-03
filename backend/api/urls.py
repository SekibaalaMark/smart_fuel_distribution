from django.urls import path
from .views import CompanyInfoView, ContactCreateView

urlpatterns = [
    path('company-info/', CompanyInfoView.as_view(), name='company-info'),

    path('contact/', ContactCreateView.as_view(), name='contact-us'),
]