from django.db import models

# Create your models here.
class LearningModule(models.Model):
    "model representing learning module"
    
    title = models.CharField(max_length=100)
    
    level = models.CharField(choices=[("basic", "Basic"), ("intermediate", "Intermediate"), ("advanced", "Advanced")], max_length=20)
    
    category = models.CharField(choices=[("vocab", "Vocabulary"), ("sentence", "Sentence"), ("culture","Culture")])
    
    media_type = models.CharField(choices=[("audio","Audio"), ("video", "Video"),("interactive", "Interactive")])
    
    content_url= models.TextField() # clloudinary  storage path