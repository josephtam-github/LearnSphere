from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from userAuth.models import Parent


class Parentprofile(models.Model):
    "parent profile management "












# class Child(models.Model):
#     """Child profile managed by parent"""
#     parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     date_of_birth = models.DateField()
#     gender = models.CharField(
#         max_length=20,
#         choices=[
#             ('male', 'Male'),
#             ('female', 'Female'),
#             ('other', 'Other'),
#             ('prefer_not_to_say', 'Prefer not to say')
#         ],
#         default='prefer_not_to_say'
#     )
#     avatar = models.CharField(max_length=100, default='default_avatar')
    
#     # Nigerian language learning specific fields
#     primary_language = models.CharField(
#         max_length=20,
#         choices=[
#             ('igbo', 'Igbo'),
#             ('hausa', 'Hausa'),
#             ('yoruba', 'Yoruba'),
#         ]
#     )
#     secondary_languages = models.JSONField(default=list)  # Other languages they want to learn
#     language_level = models.CharField(
#         max_length=20,
#         choices=[
#             ('beginner', 'Beginner'),
#             ('intermediate', 'Intermediate'),
#             ('advanced', 'Advanced'),
#         ],
#         default='beginner'
#     )
    
#     # Learning preferences
#     daily_goal_minutes = models.IntegerField(default=15)
#     preferred_learning_time = models.CharField(
#         max_length=20,
#         choices=[
#             ('morning', 'Morning'),
#             ('afternoon', 'Afternoon'),
#             ('evening', 'Evening'),
#         ],
#         default='afternoon'
#     )
    
#     # Progress tracking
#     last_activity = models.DateTimeField(null=True, blank=True)
#     total_points = models.IntegerField(default=0)
#     streak_days = models.IntegerField(default=0)
    
#     class Meta:
#         db_table = 'child_profile'
#         verbose_name = 'child'
#         verbose_name_plural = 'children'
    
#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.primary_language})"

# class ParentSettings(models.Model):
#     """Parent preferences and settings"""
#     parent = models.OneToOneField(Parent, on_delete=models.CASCADE, related_name='settings')
    
#     # Notification settings
#     email_notifications = models.BooleanField(default=True)
#     app_notifications = models.BooleanField(default=True)
#     progress_reports = models.CharField(
#         max_length=20,
#         choices=[
#             ('daily', 'Daily'),
#             ('weekly', 'Weekly'),
#             ('monthly', 'Monthly'),
#             ('never', 'Never'),
#         ],
#         default='weekly'
#     )
    
#     # Content settings
#     max_daily_screen_time = models.IntegerField(default=60)  # in minutes
#     content_difficulty = models.CharField(
#         max_length=20,
#         choices=[
#             ('age_appropriate', 'Age Appropriate'),
#             ('challenging', 'Challenging'),
#             ('easy', 'Easy'),
#         ],
#         default='age_appropriate'
#     )
    
#     class Meta:
#         db_table = 'parent_settings'

# @receiver(post_save, sender=Parent)
# def create_parent_settings(sender, instance, created, **kwargs):
#     """Automatically create settings when a new parent registers"""
#     if created:
#         ParentSettings.objects.create(parent=instance)

# class ChildProgress(models.Model):
#     """Track child's learning progress across languages and modules"""
#     child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='progress')
#     language = models.ForeignKey(Language, on_delete=models.CASCADE)
#     module = models.ForeignKey(LearningModule, on_delete=models.CASCADE)
#     completed_activities = models.JSONField(default=list)
#     mastery_percentage = models.FloatField(default=0.0)
#     last_activity_date = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'child_progress'
#         unique_together = ('child', 'module')
    
#     def __str__(self):
#         return f"{self.child.first_name} - {self.language.name} - {self.module.title}"
