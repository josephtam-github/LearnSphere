from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Language, LearningModule, LearningActivity

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'code', 'description', 'regions']

class LearningModuleSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(source='language.name', read_only=True)
    
    class Meta:
        model = LearningModule
        fields = [
            'id', 'language', 'language_name', 'title', 'description', 
            'level', 'order', 'is_active'
        ]

class LearningActivitySerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source='module.title', read_only=True)
    language_name = serializers.CharField(source='module.language.name', read_only=True)
    
    class Meta:
        model = LearningActivity
        fields = [
            'id', 'module', 'module_title', 'language_name', 'title', 
            'description', 'activity_type', 'content', 'points',
            'estimated_time_minutes', 'is_premium'
        ]
