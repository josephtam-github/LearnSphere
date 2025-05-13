from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count

from .models import OtpToken
from django.utils import timezone
from .models import Parent
from .serializer import  ParentRegistrationSerializer, VerifyOTPSerializer
from django.core.mail import send_mail

from django.contrib.auth import get_user_model
import secrets



User = get_user_model()

class ParentRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ParentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            parent = serializer.save()
            # Send verification email logic would go here
            return Response({
                'message': 'Registration successful! Please verify your email.',
                'parent_id': parent.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Verification view
@api_view(['POST'])
def verify_email(request, username):
    otp_input = request.data.get("otp")
    
    try:
        user = User.objects.get(username=username)
        
        otp = OtpToken.objects.filter(user=user).last()
        
        if otp and otp.otp_code == otp_input and otp.otp_expires_at > timezone.now():
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully"})
        
        else:
            return Response({"error": "Invalide or expired OTP"}, status=400)
    
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

@api_view(['POST'])
def resend_otp(request):
    email = request.data.get('email')
    
    try:
        user =User.objects.get(email=email)
        
        # To generate new OTP
        
        otp = OtpToken.objects.create(
            user=user,
            otp_code=secrets.token_hex(3),
            otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
        )
        
        subject = "Resend Email Verification "
        message = f"""
        
        Hi {user.username}, your new OTP is {otp.otp_code}. It expires in 5 minutes.
        http://127.0.0.1:8000/verify-email/{user.username}
        """
        sender = "godswillemmanueljames@gmail.com"
        send_mail(subject, message, sender, [user.email])
        
        return Response({"message": "OTP resent successfully"})
    
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)

# class VerifyOTPView(APIView):
#     permission_classes = [AllowAny]
#     # permission_classes = [IsAuthenticated]
    
#     def post(self, request):
#         serializer =VerifyOTPSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'message': 'Email verified successfully!'
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    