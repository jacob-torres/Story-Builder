from django import forms

from .models import Story, Scene, Character, Plot, PlotPoint
from .constants import genre_choices, mbti_choices, enneagram_choices

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
    premise = forms.CharField(required=False)

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
    premise = forms.CharField(required=False)


class NewSceneForm(forms.ModelForm):
    """Form for creating a new scene in a story."""

    class Meta:
        model = Scene
        exclude = ('story',)

        # Define fields
        # if not character_choices and not plot_point_choices:
        #     exclude = ('story', 'plot_point', 'characters')
        # elif not character_choices:
        #     exclude = ('story', 'characters')
        # elif not plot_point_choices:
        #     exclude = ('story', 'plot_point')
        # else:
        #     exclude = ('story',)

        # characters = forms.MultipleChoiceField(
        #     choices=character_choices,
        #     widget=forms.CheckboxSelectMultiple,
        #     required=False
        # )

    def __init__(self, *args, **kwargs):
        story_id = kwargs.pop('story_id', None)
        super().__init__(*args, **kwargs)

        if story_id:
            self.instance.story = Story.objects.get(pk=story_id)


class NewCharacterForm(forms.ModelForm):
    """Form for creating a new character."""

    class Meta:
        model = Character
        exclude = ('full_name',)

        # Define personality type fields
        mbti_personality = forms.ChoiceField(choices=mbti_choices)
        enneagram_personality = forms.ChoiceField(choices=enneagram_choices)

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
