from django.db import models
from userProfile.models import ChildProfile
# Create your models here.
class Streak(models.Model):
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE)
    
    current_streak = models.IntegerField(default=0)
    
    points = models.IntegerField(default=0)