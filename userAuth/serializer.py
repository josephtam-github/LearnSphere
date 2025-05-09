from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Parent
from django.core.mail import send_mail
from django.utils.timezone import now

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
        
        # Validate parent age (must be 18+)
        # from datetime import date
        # min_age = 18
        # today = date.today()
        # date_of_birth = data.get('date_of_birth')
        
        # if date_of_birth:
        #     age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        #     if age < min_age:
        #         raise serializers.ValidationError({"date_of_birth": f"You must be at least {min_age} years old to register."})
        
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
        send_mail(subject, message, "godswillemmaueljames@gmail.com", [email])

# OTP Verification Serializer
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(max_length=6, required=True)
        
    def validate(self, data):
        # Check if the OTP code is valid and not expired
        try:
            parent = Parent.objects.get(email=data['email'])
        except Parent.DoesNotExist:
            raise serializers.ValidationError({"email": "Email not registered."})
            
        if parent.otp_code != data['otp_code']:
                raise serializers.ValidationError({"otp_code": "Invalid OTP code."})
            
        if parent.otp_expiry < now():
                raise serializers.ValidationError({"otp_code": "OTP code has expired."})
            
        return data
        
    def save(self):
        # Mark the email as verified
        parent = Parent.objects.get(email=self.validated_data['email'])
        parent.is_email_verified = True
        parent.is_verified = True
        parent.otp_code = None
        parent.otp_expiry = None
        parent.save()
    

# Check push
# It is well
# check    