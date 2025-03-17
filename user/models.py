from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the built-in User model
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # Add any other profile fields you need here (address, etc.)

    def __str__(self):
        return self.user.username  # Display the username in admin interface
