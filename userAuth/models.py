from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
import uuid
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
import random

from django.utils.timezone import now, timedelta

from django.conf import settings

import secrets

class Parent(AbstractUser):
    """Parent user model with authentication"""
    email = models.EmailField(unique=True)

    is_email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    # Authentication fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'parent_user'
        verbose_name = 'parent'
        verbose_name_plural = 'parents'
        
    def __str__(self):
        return f"{self.username}  ({self.email})"
    
    # def generate_otp(self):
    #     """Generate a 6-digit OTP code and set its expiry time."""
    
        
    #     self.otp_code = str(random.randint(100000, 999999))
    #     self.otp_expiry = now() + timedelta(minutes=5)
    #     self.save()
    
     
class OtpToken(models.Model):
    """Model to store OTP tokens for users(parents)"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username