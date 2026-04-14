from django.urls import path
from .views import *

urlpatterns = [
    path('company-info/', CompanyInfoView.as_view(), name='company-info'),

    path('contact/', ContactCreateView.as_view(), name='contact-us'),
    
    
    
    # ADMIN ENDPOINTS (Dashboard side)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('admin/update-site/', AdminCompanyUpdateView.as_view()),
    path('admin/inquiries/', AdminInquiryListView.as_view()),
    path('admin/inquiries/<int:pk>/reply/', AdminReplyEmailView.as_view()),
]
