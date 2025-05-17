from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Parent

class ParentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Parent
        fields = [
            'email', 'username', 'password', 'password_confirm', 
           
        ]
    
    def validate(self, data):
        # Check that passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords don't match"})
        
      
        return data
    
    def create(self, validated_data):
        # Remove password confirmation field
        validated_data.pop('password_confirm')
        
        # Extract password to set separately
        password = validated_data.pop('password')
        
        # Create user
        parent = Parent(**validated_data)
        parent.set_password(password)
        parent.save()
        return parent