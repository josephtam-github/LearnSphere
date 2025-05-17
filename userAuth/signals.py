from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import OtpToken
from django.utils import timezone
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_otp_token(sender, instance, created, **kwargs):
    
    if created:
        if instance.is_superuser:
            pass
        else:
            OtpToken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            instance.is_active = False
            instance.save()
            
            # email credentials
            otp = OtpToken.objects.filter(user=instance).last()
            
            subject = "Email Verification"
            message = f"""
            Hi {instance.username}, Thanks for siging up! here is your OTP {otp.otp_code} it expires in 5 minutes, use the url below to redirect back to the website http://127.0.1:8000/verify-email/{instance.username}/ 
            
            Thanks, LearnSphere Team
            """
            
        
            sender = settings.EMAIL_HOST_USER
            receiver = instance.email
            
            #send email
            send_mail(
                subject, 
                message, 
                sender,
                [receiver], 
                fail_silently=False
            )