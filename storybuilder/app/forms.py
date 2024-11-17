from django import forms
from .models import Story


class NewStoryForm(forms.ModelForm):
    """Form for creating a new story."""

    class Meta:
        model = Story
        fields = ('title', 'premise', 'description', 'genre')

    # Genre field definition
    genre_choices = [
        ('1', 'Contemporary Fiction'),
        ('2', 'Literary Fiction'),
        ('3', 'Science Fiction'),
        ('4', 'Fantasy'),
        ('5', 'Romance'),
        ('6', 'Horror'),
        ('7', 'Historical Fiction'),
        ('8', 'Young Adult'),
        ('9', 'Children\'s'),
        ('10', 'Flash Fiction'),
        ('11', 'Experimental'),
        ('12', 'Game'),
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
