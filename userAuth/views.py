from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

class UserRegistrationView(generics.CreateAPIView):
    """Handle user registration"""
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Send verification email
            self.send_verification_email(user)
            
            return Response({
                "message": "Registration successful. Please check your email for verification.",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_verification_email(self, user):
        pass
        # """Send email verification link to user"""
        # verification_link = f"{settings.SITE_URL}/verify-email/{user.verification_token}"
        # send_mail(
        #     subject="Verify your email for Nigerian Language Learning Platform",
        #     message=f"Please click the link to verify your email: {verification_link}",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[user.email]
        # )
