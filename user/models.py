from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def send_initial_email(sender, instance, created, **kwargs):
    print(f"Signal Triggered for :{instance.username}, Created: {created}")
    if created and not instance._state.adding:
       
        print("New user created", instance.username)
        print(f"New user detected: {instance.username}, Email: {instance.email}")
        temporary_password = str(uuid.uuid4())[:8] 

        instance.set_password(temporary_password)
        instance.save(update_fields=["password"])  

        user_profile, created_profile = UserProfile.objects.get_or_create(user=instance)

        if created_profile:
            print("Create new UserProfile for user", instance.username)
        else:
            print("UserProfile already exists for user:", instance.username)
        
        token = default_token_generator.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        activation_url = f"http://127.0.0.1:8000/user/activate/{uid}/{token}/"  # have to replace it later with new domain

        subject = "Your Account Details"
        message = render_to_string("user/welcome_email.html", {
            'username': instance.username,
            'temporary_password': temporary_password,
            'activation_url': activation_url,  # Send the activation URL
        })

        # send_mail(subject, "", settings.EMAIL_HOST_USER, [instance.email], fail_silently=False, html_message=message)
        # send_mail(subject, "please activate your account", settings.EMAIL_HOST_USER, [instance.email], fail_silently=False, html_message=message)
        send_mail(
                subject,
                "",  # Empty string for text content (since we are using `html_message`)
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=False,
                html_message=message
            )
        # send_mail(
        #         "Test Email",
        #         "This is a test email from Django.",
        #         settings.EMAIL_HOST_USER,
        #         ["adityabhadauriya93@gmail.com"],  # Replace with your actual email
        #         fail_silently=False,
        #     )

        print("Email sent to ", instance.email)
        print("Activation link send", activation_url)
