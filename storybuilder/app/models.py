from django.db import models

# Create your models here.
max_length = 250


class Story(models.Model):
    """The story data structure, with characters, plots, worlds, and scenes."""

    # Story details
    title = models.CharField(max_length=max_length, null=False)
    description = models.TextField(null=True)
    premise = models.CharField(max_length=max_length, null=True)

    genres = models.CharField(null=True)
    word_count = models.PositiveIntegerField(default=0)
    date_started = models.DateField(auto_now_add=True)
    date_last_saved = models.DateField(auto_now=True)
    date_finished = models.DateField(null=True)

    # Relationships: One or more characters and scenes
    characters = models.ManyToManyField('Character')


class Character(models.Model):
    """Story character."""

    first_name = models.CharField(max_length=max_length, null=False)
    middle_name = models.CharField(max_length=max_length, blank=True, null=True)
    last_name = models.CharField(max_length=max_length, blank=True, null=True)
    full_name = models.CharField(null=True)

    # Demographic details
    gender = models.CharField(max_length=max_length, null=True)
    age = models.PositiveSmallIntegerField(null=True)
    ethnicity = models.CharField(max_length=max_length, null=True)
    occupation = models.CharField(max_length=max_length, null=True)
    location = models.CharField(max_length=max_length, null=True)

    # Physical details
    hair_color = models.CharField(max_length=max_length, null=True)
    eye_color = models.CharField(max_length=max_length, null=True)
    height = models.CharField(max_length=max_length, null=True)
    body_type = models.CharField(max_length=max_length, null=True)

# Personality types
    mbti_personality = models.CharField(null=True)
    enneagram_personality = models.CharField(null=True)

    # Long character description
    description = models.TextField(null=True)

    def clean(self):
        """Data cleaning method for the Character object."""
        super().clean()

        # Construct full name
        self.full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        self.full_name = ' '.join(filter(None, self.full_name.split()))


class Scene(models.Model):
    """A single unit or building block of a story."""

    title = models.CharField(max_length=max_length, null=False)
    description = models.TextField(null=True)

    # Relationships: One story and one possible plot point, one or more characters
    story = models.ForeignKey(Story, on_delete=models.CASCADE, default=None)
    plot_point = models.ForeignKey('PlotPoint', on_delete=models.SET_DEFAULT, default=None, null=True)
    characters = models.ManyToManyField(Character)


class Plot(models.Model):
    """Plots and their plot points, characters, and progressions."""

    name = models.CharField(max_length=max_length, null=False)
    description = models.TextField(null=True)

    # Relationships: One story
    story = models.OneToOneField(Story, on_delete=models.CASCADE, default=None, related_name='plot')


class PlotPoint(models.Model):
    """A single point of a story's plot."""

    name = models.CharField(max_length=max_length, null=False)
    description = models.TextField(null=True)

    # Relationships: One plot
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, default=None)


class World(models.Model):
    """Worlds and their details."""

    name = models.CharField(max_length=max_length, null=False)
    description = models.TextField(null=True)

    # Relationships: One or more stories and characters
    stories = models.ManyToManyField(Story)
    characters = models.ManyToManyField(Character)
