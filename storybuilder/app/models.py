from django.db import models

# Create your models here.
max_length = 100


class Story(models.Model):
    """The largest datatype, having characters, plots, worlds, and scenes."""

    # Story details
    title = models.CharField(max_length=max_length)
    premise = models.TextField()
    synopsis = models.TextField()
    genre = models.CharField(max_length=max_length)
    word_count = models.PositiveIntegerField(default=0)
    date_started = models.DateField(null=False, auto_now_add=True)
    date_last_saved = models.DateField(null=False, auto_now=True)
    date_finished = models.DateField(null=True, blank=True)


class Character(models.Model):
    """Story character."""

    # Names
    first_name = models.CharField(max_length=max_length)
    middle_name = models.CharField(max_length=max_length)
    last_name = models.CharField(max_length=max_length)

    # Demographic details
    gender = models.CharField(max_length=max_length)
    age = models.PositiveSmallIntegerField()
    ethnicity = models.CharField(max_length=max_length)
    occupation = models.CharField(max_length=max_length)
    location = models.CharField(max_length=max_length)

    # Physical details
    hair_color = models.CharField(max_length=max_length)
    eye_color = models.CharField(max_length=max_length)
    height = models.CharField(max_length=max_length)
    body_type = models.CharField(max_length=max_length)

    # Generate MBTI personality type combinations
    mbti_choices = []
    for e_i in ['E', 'I']:
        for n_s in ['N', 'S']:
            for f_t in ['F', 'T']:
                for j_p in ['J', 'P']:
                    mbti_choices.append(e_i + n_s + f_t + j_p)

    # Generate enneagram types 1 through 9
    enneagram_choices = [num + 1 for num in range(9)]

    mbti_personality = models.CharField(choices=mbti_choices, max_length=4)
    enneagram_personality = models.PositiveSmallIntegerField(choices=enneagram_choices)

    # Long character description
    description = models.TextField()


class Scene(models.Model):
    """A single unit or building block of a story."""

    title = models.CharField(max_length=200)
    description = models.TextField()

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

    title = models.CharField(max_length=200)
    synopsis = models.TextField()

    # Relationships: One story, many plot points
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    plot_points = models.ManyToManyField(PlotPoint)


class World(models.Model):
    """Worlds and their details."""

    name = models.CharField(max_length=100)
    description = models.TextField()

    # Relationships: One or more stories and characters
    stories = models.ManyToManyField(Story)
    characters = models.ManyToManyField(Character)
