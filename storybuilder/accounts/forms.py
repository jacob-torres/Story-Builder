from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser, UserProfile


class UserRegistrationForm(UserCreationForm):
    """Form for creating a new user account."""

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'middle_name', 'last_name']


class UserLoginForm(AuthenticationForm):
    """Form for logging in an existing user."""

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):
    """Form for updating the user profile."""

    class Meta:
        model = UserProfile
        exclude = ['user']
