from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class User(AbstractUser):
    """Extended user model with additional fields for language learning platform"""
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    date_of_birth = models.DateField(null=True)
    country = models.CharField(max_length=100, null=True)
    native_language = models.CharField(max_length=50, null=True)
    
    # Required for extending AbstractUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
        
        # Additional email validation could be added here
        return attrs

    def create(self, validated_data):
        """Create new user with encrypted password"""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user