from django import forms

from .models import Story, Scene, Character, Plot, PlotPoint
from .constants import genre_choices, mbti_choices, enneagram_choices


class StoryForm(forms.ModelForm):
    """Form for creating or updating a story."""

    class Meta:
        model = Story
        fields = ('title', 'description', 'genres', 'premise')

    genres = forms.MultipleChoiceField(
        choices=genre_choices,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    other_choice = forms.CharField(required=False)
    premise = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pre-populate fields if an instance of the object exists
        if self.instance:
            self.fields['title'].initial = self.instance.title
            self.fields['description'].initial = self.instance.description
            self.fields['premise'].initial = self.instance.premise
            self.fields['genres'].initial = self.instance.genres

    def clean(self):
        """Data cleaning function for story form."""

        print("**********************************")
        print("Story Form Clean Method")
        clean_data = super().clean()

        # Process other genre choice
        if 'genres' in clean_data:
            genre_choices = list(clean_data['genres'])
            if 'Other' in genre_choices:
                if not clean_data['other_choice']:
                    raise forms.ValidationError('Please specify your other choice.')
                genre_choices.remove('Other')
                genre_choices.append(clean_data['other_choice'])
            clean_data['genres'] = genre_choices

        print(f"clean_data: {clean_data}")
        return clean_data
    

class SceneForm(forms.ModelForm):
    """Form for creating a new scene in a story."""

    class Meta:
        model = Scene
        exclude = ('story',)

    def __init__(self, *args, **kwargs):
        story_id = kwargs.pop('story_id', None)
        super().__init__(*args, **kwargs)

        # Define the story that the object is associated with
        if story_id:
            self.instance.story = Story.objects.get(pk=story_id)

        # Pre-populate fields if an instance of the object exists
        if self.instance:
            self.fields['title'].initial = self.instance.title
            self.fields['description'].initial = self.instance.description
            self.fields['characters'].initial = self.instance.characters
            self.fields['plot_point'].initial = self.instance.plot_point


class CharacterForm(forms.ModelForm):
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

        # Define the story that the object is associated with
        if story_id:
            self.instance.story = Story.objects.get(pk=story_id)

        # Pre-populate fields if an instance of the object exists
        if self.instance:
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['middle_name'].initial = self.instance.middle_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['gender'].initial = self.instance.gender
            self.fields['age'].initial = self.instance.age
            self.fields['ethnicity'].initial = self.instance.ethnicity
            self.fields['occupation'].initial = self.instance.occupation
            self.fields['location'].initial = self.instance.location
            self.fields['hair_color'].initial = self.instance.hair_color
            self.fields['eye_color'].initial = self.instance.eye_color
            self.fields['height'].initial = self.instance.height
            self.fields['body_type'].initial = self.instance.body_type
            self.fields['mbti_personality'].initial = self.instance.mbti_personality
            self.fields['enneagram_personality'].initial = self.instance.enneagram_personality
            self.fields['description'].initial = self.instance.description


class PlotForm(forms.ModelForm):
    """Form for creating a new plot."""

    class Meta:
        model = Plot
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        story_id = kwargs.pop('story_id', None)
        super().__init__(*args, **kwargs)

        # Define the story that the object is associated with
        if story_id:
            self.instance.story = Story.objects.get(pk=story_id)

        # Pre-populate fields if an instance of the object exists
        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['description'].initial = self.instance.description
            self.fields['plot_points'].initial = self.instance.plot_points


class PlotPointForm(forms.ModelForm):
    """Form for creating a new plot point."""

    class Meta:
        model = PlotPoint
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        story_id = kwargs.pop('story_id', None)
        plot_id = kwargs.pop('plot_id', None)
        super().__init__(*args, **kwargs)

        # Define the story and the plot that the object is associated with
        if story_id:
            self.instance.story = Story.objects.get(pk=story_id)
        if plot_id:
            self.instance.plot = Plot.objects.get(pk=plot_id)

        # Pre-populate fields if an instance of the object exists
        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['description'].initial = self.instance.description
