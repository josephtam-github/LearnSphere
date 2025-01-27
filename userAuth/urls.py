from django.urls import path
from .views import (
    UserRegistrationView, 
    user_login, 
    # verify_email,
    UserProfileView,
    UserLogoutView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', user_login, name='login'),
    # path('verify-email/<uuid:token>/', verify_email, name='verify-email'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]