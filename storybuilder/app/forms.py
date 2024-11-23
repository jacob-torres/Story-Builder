from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Story


class NewStoryForm(forms.ModelForm):
    """Form for creating a new story."""

    class Meta:
        model = Story
        fields = ('title', 'description', 'genres')

    genres = forms.MultipleChoiceField(
        choices=Story.genre_choices,
        widget=forms.CheckboxSelectMultiple
    )
    other_choice = forms.CharField(required=False)
    premise = forms.CharField(max_length=250, required=False)

    def clean(self):
        """Data cleaning function."""

        clean_data = super().clean()
        genre_choices = list(clean_data['genres'])
        if 'Other' in genre_choices:
            if not clean_data['other_choice']:
                raise forms.ValidationError('Please specify your other choice.')
            genre_choices.remove('Other')
            genre_choices.append(clean_data['other_choice'])

        clean_data['genres'] = ', '.join(genre_choices)
        return clean_data


class UpdateStoryForm(forms.ModelForm):
    """Form for updating a story."""

    class Meta:
        model = Story
        fields = ('title', 'description', 'genres')

    # Define optional fields
    premise = forms.CharField(max_length=250, required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        if instance:
            self.initial['title'] = instance.title
            self.initial['description'] = instance.description
            self.initial['genres'] = instance.genres.all().value_list('id', flat=True)
