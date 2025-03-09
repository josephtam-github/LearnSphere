from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    """Nigerian language data model"""
    name = models.CharField(max_length=50)  # Igbo, Hausa, Yoruba
    code = models.CharField(max_length=10, unique=True)  # ibo, hau, yor
    description = models.TextField()
    regions = models.JSONField(default=list)  # Regions where the language is spoken
    
    class Meta:
        db_table = 'language'
    
    def __str__(self):
        return self.name

class LearningModule(models.Model):
    """Learning modules for each language"""
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=100)
    description = models.TextField()
    level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ]
    )
    order = models.IntegerField()  # Sequence within curriculum
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'learning_module'
        unique_together = ('language', 'order')
        ordering = ['language', 'order']
    
    def __str__(self):
        return f"{self.language.name} - {self.title} ({self.level})"

class LearningActivity(models.Model):
    """Individual learning activities within modules"""
    module = models.ForeignKey(LearningModule, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=100)
    description = models.TextField()
    activity_type = models.CharField(
        max_length=30,
        choices=[
            ('vocabulary', 'Vocabulary Learning'),
            ('listening', 'Listening Exercise'),
            ('speaking', 'Speaking Practice'),
            ('quiz', 'Quiz'),
            ('game', 'Interactive Game'),
            ('story', 'Story Reading'),
            ('culture', 'Cultural Learning'),
        ]
    )
    content = models.JSONField()  # Structured content for the activity
    points = models.IntegerField(default=10)
    estimated_time_minutes = models.IntegerField(default=5)
    is_premium = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'learning_activity'
        ordering = ['module', 'id']
    
    def __str__(self):
        return f"{self.module.language.name} - {self.title} ({self.activity_type})"
