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

class Parent(AbstractUser):
    """Parent user model with authentication"""
    email = models.EmailField(unique=True)

    is_email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    # OTP Fields
    otp_code =models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
        
    # Authentication fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'parent_user'
        verbose_name = 'parent'
        verbose_name_plural = 'parents'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def generate_otp(self):
        """Generate a 6-digit OTP code and set its expiry time."""
    
        
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_expiry = now() + timedelta(minutes=5)
        self.save()
     
