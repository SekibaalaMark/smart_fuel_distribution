from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import *
from .serializers import *
from .permissions import *

# views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# --- COMPANY INFO MANAGEMENT ---

class AdminCompanyUpdateView(APIView):
    permission_classes = [IsSuperUser] # Only Admins allowed

    def put(self, request):
        profile = CompanyProfile.objects.first()
        # If no profile exists, we create one; otherwise, update the existing one.
        serializer = CompanyProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class AdminInquiryListView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        # Admin views all emails sent by clients
        inquiries = ContactInquiry.objects.all().order_by('-created_at')
        serializer = ContactInquirySerializer(inquiries, many=True)
        return Response(serializer.data)




from django.core.mail import send_mail
from django.conf import settings

class AdminReplyEmailView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request, pk):
        try:
            inquiry = ContactInquiry.objects.get(pk=pk)
            reply_text = request.data.get('message')

            if not reply_text:
                return Response({"error": "Message body is empty"}, status=400)

            # Send actual email to the user's inbox
            send_mail(
                subject=f"Re: {inquiry.subject}",
                message=reply_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[inquiry.email], # The client's email from the DB
                fail_silently=False, # Set to False to see errors if the SMTP fails
            )

            # Save reply to DB for the Admin to see history
            inquiry.admin_reply = reply_text
            inquiry.is_resolved = True
            inquiry.save()

            return Response({"status": "Email sent to client's inbox!"})

        except ContactInquiry.DoesNotExist:
            return Response({"error": "Inquiry not found"}, status=404)



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
                    recipient_list=['sekibaalamark44@gmail.com'], # The company's email
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
    
    
    
    
    
