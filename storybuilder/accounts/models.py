from django.contrib.auth.models import AbstractUser
from django.db import models


# Length constants
tiny_length = 30
short_length = 100
mid_length = 250
long_length = 500


class CustomUser(AbstractUser):
    """Custom User model based on AbstractUser."""

    email = models.EmailField(unique=True, default=None)
    first_name = models.CharField(max_length=short_length, default=None)
    last_name = models.CharField(max_length=short_length, default=None)


class UserProfile(models.Model):
    """User profile model for each custom user object."""

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=None, related_name='profile')
    bio = models.TextField(blank=True, default=None)
    website = models.URLField(blank=True, default=None)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
