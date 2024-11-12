from django import forms


class LoginForm(forms.Form):
    """Login form."""

    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

