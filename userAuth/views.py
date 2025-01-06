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



@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """Handle user login and return JWT tokens"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(email=email, password=password)
    
    if user is not None:
        if not user.is_email_verified:
            return Response({
                "error": "Please verify your email before logging in."
            }, status=status.HTTP_403_FORBIDDEN)
            
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'email': user.email,
                'username': user.username
            }
        })
    else:
        return Response({
            "error": "Invalid email or password"
        }, status=status.HTTP_401_UNAUTHORIZED)
