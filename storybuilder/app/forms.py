from django import forms
from .models import Story

# Global variables
max_length  = 250

# Genre field definition
genre_choices = [
    ('Contemporary Fiction', 'Contemporary Fiction'),
    ('Literary Fiction', 'Literary Fiction'),
    ('Mystery', 'Mystery'),
    ('Thriller', 'Thriller'),
    ('Science Fiction', 'Science Fiction'),
    ('Fantasy', 'Fantasy'),
    ('Romance', 'Romance'),
    ('Horror', 'Horror'),
    ('Crime', 'Crime'),
    ('Historical Fiction', 'Historical Fiction'),
    ('Young Adult', 'Young Adult'),
    ('Children\'s', 'Children\'s'),
    ('Memoir', 'Memoir'),
    ('Biography', 'Biography'),
    ('History', 'History'),
    ('True Crime', 'True Crime'),
    ('Flash Fiction', 'Flash Fiction'),
    ('Erotica', 'Erotica'),
    ('Experimental', 'Experimental'),
    ('Game', 'Game'),
    ('Other', 'Other (Use a comma-separated list to include more than one genre.)')
]


class NewStoryForm(forms.ModelForm):
    """Form for creating a new story."""

    class Meta:
        model = Story
        fields = ('title', 'description', 'genres')

    genres = forms.MultipleChoiceField(
        choices=genre_choices,
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
        fields = ('title', 'description', 'genres', 'premise')

    # Define optional fields
    premise = forms.CharField(max_length=max_length, required=False)
