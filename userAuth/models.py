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

     # Add related_names to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
     
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    
    class Meta:
        db_table = 'custom_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

class UserProfile(models.Model):
    """Additional user preferences and learning goals"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_goal_minutes = models.IntegerField(default=15)
    preferred_learning_time = models.CharField(
        max_length=20,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
        ],
        default='morning'
    )
    target_languages = models.JSONField(default=list)  # List of language codes
    notification_preferences = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.user.email}'s Profile"
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a profile when a new user is registered"""
    if created:
        UserProfile.objects.create(user=instance)
