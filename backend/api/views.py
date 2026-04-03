# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import ContactInquirySerializer

class ContactCreateView(APIView):
    def post(self, request):
        serializer = ContactInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Send Email
            send_mail(
                subject=f"New Inquiry: {serializer.validated_data['subject']}",
                message=serializer.validated_data['message'],
                from_email=serializer.validated_data['email'],
                recipient_list=['sekibaalamark44@gmail.com'],
            )
            return Response({"message": "Sent successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)