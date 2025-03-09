from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
import uuid
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

class Parent(AbstractUser):
    """Parent user model with authentication"""
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    country = CountryField(default='NG')  # Default to Nigeria
    state = models.CharField(max_length=50, blank=True, null=True)
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
        return f"{self.first_name} {self.last_name} ({self.email})"

