from django import forms
from .models import Story


class NewStoryForm(forms.ModelForm):
    """Form for creating a new story."""

    class Meta:
        model = Story
        fields = ('title', 'premise', 'description', 'genre')

    # Genre field definition
    genre_choices = [
        ('Contemporary Fiction', 'Contemporary Fiction'),
        ('Literary Fiction', 'Literary Fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Romance', 'Romance'),
        ('Horror', 'Horror'),
        ('Historical Fiction', 'Historical Fiction'),
        ('Young Adult', 'Young Adult'),
        ('Children\'s', 'Children\'s'),
        ('Flash Fiction', 'Flash Fiction'),
        ('Experimental', 'Experimental'),
        ('Game', 'Game'),
        ('other', 'Other (Specify)')
    ]

    genre = forms.MultipleChoiceField(
        choices=genre_choices,
        widget=forms.CheckboxSelectMultiple
    )
    other_choice = forms.CharField(required=False)

    def clean(self):
        """Data cleaning function."""

        clean_data = super().clean()
        if 'other' in clean_data['genre']:
            if not clean_data['other_choice']:
                raise forms.ValidationError('Please specify your other choice.')
        return clean_data
