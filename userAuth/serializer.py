from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Handle user registration with password validation"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)