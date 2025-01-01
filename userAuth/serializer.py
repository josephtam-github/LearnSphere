from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Handle user registration with password validation"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'date_of_birth', 
                 'country', 'native_language')
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        """Validate password match and email format"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return attrs

    def create(self, validated_data):
        """Create new user with encrypted password"""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user