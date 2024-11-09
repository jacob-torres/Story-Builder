from django.db import models

# Create your models here.
max_length = 100


class Character(models.Model):
    """Story character."""

    first_name = models.CharField(max_length=max_length, blank=False)
    middle_name = models.CharField(max_length=max_length, blank=True)
    last_name = models.CharField(max_length=max_length, blank=True)

    # Demographic details
    gender = models.CharField(max_length=max_length, blank=True)
    age = models.PositiveSmallIntegerField(null=True)
    ethnicity = models.CharField(max_length=max_length, blank=True)
    occupation = models.CharField(max_length=max_length, blank=True)
    location = models.CharField(max_length=max_length, blank=True)

    # Physical details
    hair_color = models.CharField(max_length=max_length, blank=True)
    eye_color = models.CharField(max_length=max_length, blank=True)
    height = models.CharField(max_length=max_length, blank=True)
    body_type = models.CharField(max_length=max_length, blank=True)

    # Generate MBTI personality type combinations
    mbti_choices = []
    for e_i in ['E', 'I']:
        for n_s in ['N', 'S']:
            for f_t in ['F', 'T']:
                for j_p in ['J', 'P']:
                    mbti_choices.append(e_i + n_s + f_t + j_p)

    # Generate enneagram types 1 through 9
    enneagram_choices = [num + 1 for num in range(9)]

    mbti_personality = models.CharField(choices=mbti_choices, max_length=4, null=True)
    enneagram_personality = models.PositiveSmallIntegerField(choices=enneagram_choices, null=True)

    # Long character description
    description = models.TextField(blank=True)


class Story(models.Model):
    """The story data structure, with characters, plots, worlds, and scenes."""

    # Story details
    title = models.CharField(max_length=max_length, blank=False)
    premise = models.TextField(blank=True)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=max_length, blank=True)
    word_count = models.PositiveIntegerField(default=0)
    date_started = models.DateField(auto_now_add=True)
    date_last_saved = models.DateField(auto_now=True)
    date_finished = models.DateField(null=True)

    # Relationships: One or more characters, plots, and scenes
    characters = models.ManyToManyField(Character)


class Scene(models.Model):
    """A single unit or building block of a story."""

    title = models.CharField(max_length=max_length, blank=False)
    description = models.TextField(blank=True)

    # Relationships: One story, one or more characters
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    characters = models.ManyToManyField(Character)


class PlotPoint(models.Model):
    """A single point of a story's plot."""

    name = models.CharField(max_length=max_length, blank=False)
    description = models.TextField(blank=True)

    # Relationships: One or more scenes
    scenes = models.ManyToManyField(Scene)


class Plot(models.Model):
    """Plots and their plot points, characters, and progressions."""

    name = models.CharField(max_length=max_length, blank=False)
    description = models.TextField(blank=True)

    # Relationships: One or more stories, many plot points
    stories = models.ManyToManyField(Story)
    plot_points = models.ManyToManyField(PlotPoint)


class World(models.Model):
    """Worlds and their details."""

    name = models.CharField(max_length=max_length, blank=False)
    description = models.TextField(blank=True)

    # Relationships: One or more stories and characters
    stories = models.ManyToManyField(Story)
    characters = models.ManyToManyField(Character)


class Collection(models.Model):
    """Collection of stories."""

    name = models.CharField(max_length=max_length, blank=False)
    description = models.TextField(blank=True)

    # Relationships: One or more stories
    stories = models.ManyToManyField(Story)
