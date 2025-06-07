from django.urls import path, include


from userAuth.views import ParentRegistrationView, verify_email, resend_otp

from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



def redirect_to_docs(request):
    return redirect('https://documenter.getpostman.com/view/24232846/2sAYX8KMrD')



# API v1 patterns
v1_patterns = [
    # Authentication endpoints
    path('register/', ParentRegistrationView.as_view(), name='parent-registration'),
    
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('token/refresh', TokenRefreshView.as_view, name='token refresh'),
    
    path('verify-email/<str:username>/', verify_email, name='verify_email')
    
    ##

    
    
  
]

urlpatterns = [
    # API Documentation redirect
    path('', redirect_to_docs, name='api-docs'),
    
    # Version 1 API
    path('v1/', include(v1_patterns)),
]