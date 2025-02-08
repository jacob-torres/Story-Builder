from django import forms

from accounts.models import CustomUser

from .models import Story, Scene, Character, Plot, PlotPoint
from .constants import genre_choices, mbti_choices, enneagram_choices


class StoryForm(forms.ModelForm):
    """Form for creating or updating a story."""

    class Meta:
        model = Story
        fields = ['title', 'description', 'premise', 'genres']

    genres = forms.MultipleChoiceField(
        choices=genre_choices,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    other_choice = forms.CharField(required=False)
    premise = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        author_id = kwargs.pop('author_id', None)
        super().__init__(*args, **kwargs)

        # Pre-populate fields if an instance of the object exists
        if self.instance:
            self.fields['title'].initial = self.instance.title
            self.fields['description'].initial = self.instance.description
            self.fields['premise'].initial = self.instance.premise
            self.fields['genres'].initial = self.instance.genres

            # Define the story that the object is associated with
            if author_id:
                self.instance.author = CustomUser.objects.get(id=author_id)

    def clean(self):
        """Override the clean method for the story form."""

        print("**********************************")
        print("Story Form Clean Method")

        cleaned_data = super().clean()
        print(f"Data before genre cleaning: {cleaned_data}")

        # Process other genre choice
        genre_choices = list(cleaned_data['genres'])
        if 'Other' in genre_choices:
            if not cleaned_data['other_choice']:
                raise forms.ValidationError('Please specify your other choice.')
            genre_choices.remove('Other')
            genre_choices.append(cleaned_data['other_choice'])
        cleaned_data['genres'] = genre_choices

        print(f"cleaned_data: {cleaned_data}")
        return cleaned_data
    

class SceneForm(forms.ModelForm):
    """Form for creating a new scene in a story."""

    class Meta:
        model = Scene
        exclude = ['story', 'order']

    def __init__(self, *args, **kwargs):
        story_slug = kwargs.pop('story_slug', None)
        author_id = kwargs.pop('author_id', None)
        super().__init__(*args, **kwargs)

        # Define the story that the object is associated with
        if story_slug:
            self.instance.story = Story.objects.get(slug=story_slug, author_id=author_id)

        # Pre-populate fields if an instance of the object exists
        if self.instance:
            self.fields['title'].initial = self.instance.title
            self.fields['description'].initial = self.instance.description


class CharacterForm(forms.ModelForm):
    """Form for creating a new character."""

    class Meta:
        model = Character
        exclude = ['full_name', 'story', 'slug']

        # Define personality type fields
        mbti_personality = forms.ChoiceField(choices=mbti_choices)
        enneagram_personality = forms.ChoiceField(choices=enneagram_choices)

    def __init__(self, *args, **kwargs):
        story_slug = kwargs.pop('story_slug', None)
        author_id = kwargs.pop('author_id', None)
        super().__init__(*args, **kwargs)

        # Define the story that the object is associated with
        if story_slug and author_id:
            self.instance.story = Story.objects.get(slug=story_slug, author_id=author_id)

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
    """Form for updating a story plot."""

    class Meta:
        model = Plot
        exclude = ['story']

    def __init__(self, *args, **kwargs):
        story_slug = kwargs.pop('story_slug', None)
        super().__init__(*args, **kwargs)

        # Pre-populate fields if an instance of the object exists
        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['description'].initial = self.instance.description

            # Define the story that the object is associated with
            if story_slug:
                self.instance.story = Story.objects.get(slug=story_slug)


class PlotPointForm(forms.ModelForm):
    """Form for creating a new plot point."""

    class Meta:
        model = PlotPoint
        exclude = ['plot', 'order']

    def __init__(self, *args, **kwargs):
        plot_id = kwargs.pop('plot_id', None)
        super().__init__(*args, **kwargs)

        # Pre-populate fields if an instance of the object exists
        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['description'].initial = self.instance.description

            # Define the plot that the object is associated with
            if plot_id:
                self.instance.plot = Plot.objects.get(pk=plot_id)


class WordCountForm(forms.ModelForm):
    """Form for updating the story word count."""

    word_count = forms.IntegerField(min_value=0, label='New Word Count')

    class Meta:
        model = Story
        fields = ['word_count']


class SceneNoteForm(forms.ModelForm):
    """Form for adding a new note to a scene."""

    note = forms.CharField(max_length=500, label='New Scene Note')

    class Meta:
        model = Scene
        fields = ['note']


class SceneCharacterForm(forms.ModelForm):
    """Form for adding characters to a specific scene."""

    class Meta:
        model = Scene
        fields = ['characters']

    def __init__(self, *args, **kwargs):
        story_slug = kwargs.pop('story_slug', None)
        super().__init__(*args, **kwargs)

        # Pre-populate fields if an instance of the object exists
        if self.instance:
            self.fields['characters'].initial = self.instance.characters

            # Define the story that the object is associated with
            if story_slug:
                self.instance.story = Story.objects.get(slug=story_slug)

        # Define the character multiple choice field
        character_choices = [
            (character.full_name, character.full_name) for character in Character.objects.filter(story=self.instance.story)
        ]

        characters = forms.MultipleChoiceField(
            choices=character_choices,
            widget=forms.CheckboxSelectMultiple
        )
