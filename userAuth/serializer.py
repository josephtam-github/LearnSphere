from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Parent
from django.core.mail import send_mail

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
            'first_name', 'last_name', 'phone_number', 'date_of_birth',
            'country', 'state'
        ]
    
    def validate(self, data):
        # Check that passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords don't match"})
        
        # Validate parent age (must be 18+)
        from datetime import date
        min_age = 18
        today = date.today()
        date_of_birth = data.get('date_of_birth')
        
        if date_of_birth:
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < min_age:
                raise serializers.ValidationError({"date_of_birth": f"You must be at least {min_age} years old to register."})
        
        return data
    
    def create(self, validated_data):
        # Remove password confirmation field
        validated_data.pop('password_confirm')
        
        # Extract password to set separately
        password = validated_data.pop('password')
        
        # Create user
        parent = Parent(**validated_data)
        parent.set_password(password)
        parent.is_verified = False
        parent.generate_otp()
        parent.save()
        
        # Send OTP to email
        
        self.send_otp_email(parent.email, parent.otp_code)
        
        return parent
    
    def send_otp_email(self, email, otp):
        """Send OTP email to the user."""
        subject = "Verify Your Email with OTP"
        message = f"Your OTP code is {otp}. It will expire in 5 minutes."
        send_mail(subject, message, "noreply@learnsphere.com", [email])