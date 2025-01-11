from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser, UserProfile


class UserRegistrationForm(forms.ModelForm):
    """Form for creating a new user account."""

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_password2(self):
        """Method for cleaning the confirm-password field."""

        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2


class UserLoginForm(AuthenticationForm):
    """Form for logging in an existing user."""

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class UserProfileForm(forms.ModelForm):
    """Form for updating the user profile."""

    class Meta:
        model = UserProfile
        fields = '__all__'
