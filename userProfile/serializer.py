from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Child, ParentSettings, ChildProgress

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'avatar', 'primary_language', 'secondary_languages', 
            'language_level', 'daily_goal_minutes', 'preferred_learning_time'
        ]
        read_only_fields = ['id', 'total_points', 'streak_days', 'last_activity']
    
    def validate_date_of_birth(self, value):
        # Children should be under 18
        from datetime import date
        max_age = 18
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if age >= max_age:
            raise serializers.ValidationError(f"Child must be under {max_age} years old.")
            
        # Check for very young children (e.g., not yet born)
        if value > today:
            raise serializers.ValidationError("Birth date cannot be in the future.")
            
        return value

class ParentSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentSettings
        fields = [
            'email_notifications', 'app_notifications', 'progress_reports',
            'max_daily_screen_time', 'content_difficulty'
        ]

class ChildProgressSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(source='language.name', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    child_name = serializers.CharField(source='child.first_name', read_only=True)
    
    class Meta:
        model = ChildProgress
        fields = [
            'id', 'child', 'child_name', 'language', 'language_name', 'module',
            'module_title', 'completed_activities', 'mastery_percentage',
            'last_activity_date'
        ]
        read_only_fields = ['mastery_percentage', 'last_activity_date']
