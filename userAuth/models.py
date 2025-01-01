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
