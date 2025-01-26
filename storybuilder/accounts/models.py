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
    middle_name = models.CharField(max_length=short_length, blank=True, null=True)
    last_name = models.CharField(max_length=short_length, default=None)
    full_name = models.CharField(max_length=long_length, null=True)

    # Add related_name args for groups and permissions fields to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        help_text='The groups this user belongs to.',
        related_name='custom_user_set'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_name='custom_user_set'
    )

    def __str__(self):
        """Override string method to display user full name."""
        return self.full_name

    def clean(self):
        """Data cleaning method for the custom user object."""
        super().clean()

        # Construct full name
        names = [self.first_name, self.middle_name, self.last_name]
        for name in names:
            if not name:
                names.remove(name)

        self.full_name = ' '.join(filter(None, names))


class UserProfile(models.Model):
    """User profile model for each custom user object."""

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=None, related_name='profile')
    bio = models.TextField(blank=True, default=None)
    website = models.URLField(blank=True, default=None)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
