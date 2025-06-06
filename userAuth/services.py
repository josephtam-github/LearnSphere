from .models import OtpToken
from django.utils import timezone
import secrets
from django.core.mail import send_mail


def generate_and_send_otp(user):
     
        # To generate new OTP
        
    otp = OtpToken.objects.create(
        user=user,
        otp_code=secrets.token_hex(3),
        otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
    )
        
    subject = "Resend Email Verification "
    message = f"""
    Hi {user.username}, your new OTP is {otp.otp_code}. It expires in 5 minutes.
    http://127.0.0.1:8000/verify-email/{user.username}
    """
        
    sender = "godswillemmanueljames@gmail.com"
    send_mail(subject, message, sender, [user.email])
    
    return otp