from django import forms
from .models import Story


class NewStoryForm(forms.ModelForm):
    """Form for creating a new story."""

    class Meta:
        model = Story
        fields = ('title', 'description', 'genres')

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
        ('Other', 'Other (Use a comma-separated list to include more than one genre.)')
    ]

    genres = forms.MultipleChoiceField(
        choices=genre_choices,
        widget=forms.CheckboxSelectMultiple
    )
    other_choice = forms.CharField(required=False)

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
