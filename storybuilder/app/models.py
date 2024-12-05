from django.db import models
from django.contrib.postgres.fields import ArrayField

from .constants import genre_choices, mbti_choices, enneagram_choices

# Create your models here.
tiny_length = 30
short_length = 100
mid_length = 250
long_length = 500


class Story(models.Model):
    """The story data structure, with characters, plots, worlds, and scenes."""

    # Story details
    title = models.CharField(max_length=short_length, null=False)
    description = models.TextField(max_length=long_length, null=True)
    premise = models.CharField(max_length=mid_length, null=True)

    genres = ArrayField(
        models.CharField(max_length=tiny_length),
        blank=True,
        null=True
    )

    word_count = models.PositiveIntegerField(default=0)
    date_started = models.DateField(auto_now_add=True)
    date_last_saved = models.DateField(auto_now=True)
    date_finished = models.DateField(null=True)

    # Relationships: One or more characters, genres,  and scenes
    characters = models.ManyToManyField('Character', blank=True)


class Character(models.Model):
    """Story character."""

    first_name = models.CharField(max_length=tiny_length, null=False)
    middle_name = models.CharField(max_length=tiny_length, blank=True, null=True)
    last_name = models.CharField(max_length=tiny_length, blank=True, null=True)
    full_name = models.CharField(max_length=short_length, null=True)

    # Demographic details
    gender = models.CharField(max_length=short_length, blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    ethnicity = models.CharField(max_length=short_length, blank=True, null=True)
    occupation = models.CharField(max_length=short_length, blank=True, null=True)
    location = models.CharField(max_length=short_length, blank=True, null=True)

    # Physical details
    hair_color = models.CharField(max_length=short_length, blank=True, null=True)
    eye_color = models.CharField(max_length=short_length, blank=True, null=True)
    height = models.CharField(max_length=short_length, blank=True, null=True)
    body_type = models.CharField(max_length=short_length, blank=True, null=True)

# Personality types
    mbti_personality = models.CharField(choices=mbti_choices, blank=True, null=True)
    enneagram_personality = models.CharField(choices=enneagram_choices, blank=True, null=True)

    # Long character description
    description = models.TextField(max_length=long_length, null=True)

    def clean(self):
        """Data cleaning method for the Character object."""
        super().clean()

        # Construct full name
        names = [self.first_name, self.middle_name, self.last_name]
        for name in names:
            if not name:
                names.remove(name)

        if len(names) == 1:
            self.full_name = self.first_name
        else:
            self.full_name = ' '.join(filter(None, names))


class Scene(models.Model):
    """A single unit or building block of a story."""

    title = models.CharField(max_length=short_length, null=False)
    description = models.TextField(max_length=long_length, null=True)

    # Relationships: One story and one possible plot point, one or more characters
    story = models.ForeignKey(Story, on_delete=models.CASCADE, default=None)
    plot_point = models.ForeignKey('PlotPoint', on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    characters = models.ManyToManyField(Character, blank=True)


class Plot(models.Model):
    """Plots and their plot points, characters, and progressions."""

    name = models.CharField(max_length=short_length, null=False)
    description = models.TextField(max_length=long_length, null=True)

    # Relationships: One story
    story = models.OneToOneField(Story, on_delete=models.CASCADE, default=None, related_name='plot')


class PlotPoint(models.Model):
    """A single point of a story's plot."""

    name = models.CharField(max_length=short_length, null=False)
    description = models.TextField(max_length=long_length, null=True)

    # Relationships: One plot
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, default=None)


class World(models.Model):
    """Worlds and their details."""

    name = models.CharField(max_length=short_length, null=False)
    description = models.TextField(max_length=long_length, null=True)

    # Relationships: One or more stories and characters
    stories = models.ManyToManyField(Story, blank=True)
    characters = models.ManyToManyField(Character, blank=True)
