from django import forms

from .models import Story, Scene, Character, Plot, PlotPoint

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

# Story choices
story_choices = [
    (story.title, story.title) for story in Story.objects.all()
]

# Character field definition
character_choices = [
    (character.full_name, character.full_name) for character in Character.objects.all()
]

# Plot point choices
plot_point_choices = [
    (plot_point.name, plot_point.name) for plot_point in PlotPoint.objects.all()
]

# MBTI personality types
mbti_choices = [
    ('INTJ: The Architect', 'INTJ: The Architect'),
    ('INTP: The Logician', 'INTP: The Logician'),
    ('ENTJ: The Commander', 'ENTJ: The Commander'),
    ('ENTP: The Visionary', 'ENTP: The Visionary'),
    ('INFJ: The Advocate', 'INFJ: The Advocate'),
    ('INFP: The Idealist', 'INFP: The Idealist'),
    ('ENFJ: The Giver', 'ENFJ: The Giver'),
    ('ENFP: The Enthusiast', 'ENFP: The Enthusiast'),
    ('ISTJ: The Duty Fulfiller', 'ISTJ: The Duty Fulfiller'),
    ('ISFJ: The Protector', 'ISFJ: The Protector'),
    ('ESTJ: The Executive', 'ESTJ: The Executive'),
    ('ESFJ: The Caregiver', 'ESFJ: The Caregiver'),
    ('ISTP: The Craftsman', 'ISTP: The Craftsman'),
    ('ISFP: The Artist', 'ISFP: The Artist')
]

# Enneagram personality types
enneagram_choices = [
    ('1: The Reformer', '1: The Reformer'),
    ('2: The Helper', '2: The Helper'),
    ('3: The Achiever', '3: The Achiever'),
    ('4: The Romantic', '4: The Romantic'),
    ('5: The Investigator', '5: The Investigator'),
    ('6: The Skeptic', '6: The Skeptic'),
    ('7: The Enthusiast', '7: The Enthusiast'),
    ('8: The Challenger', '8: The Challenger'),
    ('9: The Peacemaker', '9: The Peacemaker')
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
    premise = forms.CharField(max_length=max_length, required=False)

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


class NewSceneForm(forms.ModelForm):
    """Form for creating a new scene in a story."""

    class Meta:
        model = Scene

        # Define fields
        if not character_choices and not plot_point_choices:
            exclude = ('story', 'plot_point', 'characters')
        elif not character_choices:
            exclude = ('story', 'characters')
        elif not plot_point_choices:
            exclude = ('story', 'plot_point')
        else:
            exclude = ('story',)

        characters = forms.MultipleChoiceField(
            choices=character_choices,
            widget=forms.CheckboxSelectMultiple,
            required=False
        )

    def __init__(self, *args, **kwargs):
        story_id = kwargs.pop('story_id', None)
        super().__init__(*args, **kwargs)

        if story_id:
            self.instance.story = Story.objects.get(pk=story_id)


class NewCharacterForm(forms.ModelForm):
    """Form for creating a new character."""

    class Meta:
        model = Character
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        story_id = kwargs.pop('story_id', None)
        super().__init__(*args, **kwargs)

        if story_id:
            self.instance.story = Story.objects.get(pk=story_id)


class NewPlotForm(forms.ModelForm):
    """Form for creating a new plot."""

    class Meta:
        model = Plot
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        story_id = kwargs.pop('story_id', None)
        super().__init__(*args, **kwargs)

        if story_id:
            self.instance.story = Story.objects.get(pk=story_id)


class NewPlotPointForm(forms.ModelForm):
    """Form for creating a new plot point."""

    class Meta:
        model = PlotPoint
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        story_id = kwargs.pop('story_id', None)
        plot_id = kwargs.pop('plot_id', None)
        super().__init__(*args, **kwargs)

        if story_id:
            self.instance.story = Story.objects.get(pk=story_id)
        if plot_id:
            self.instance.plot = Plot.objects.get(pk=plot_id)
