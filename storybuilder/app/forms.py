from django import forms
from .models import CustomUser


class LoginForm(forms.Form):
    """Login form."""

    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class SignupForm(forms.ModelForm):
    """Signup form."""

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
