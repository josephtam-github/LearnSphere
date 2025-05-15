from django.db import models
from userProfile.models import ParentProfile
# Create your models here.

class Subscription(models.Model):
    """Sunscription model for managing subscription plans"""
    
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='subscriptions')
    
    plan = models.CharField(choices=[("weekly", "Weekly"), ("monthly", "Monthly"), ("yearly", "Yearly")], max_length=20)
    
    # amount = models.DecimalField(...)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_active = models.BooleanField(default=True)
    
    start_date = models.DateTimeField()
    
    end_date = models.DateTimeField()