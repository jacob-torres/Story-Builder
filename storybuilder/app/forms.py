from django import forms
from .models import Story


class NewStoryForm(forms.ModelForm):
    """Form for creating a new story."""

    class Meta:
        model = Story
        fields = '__all__'
