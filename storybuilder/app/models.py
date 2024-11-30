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
    middle_name = models.CharField(max_length=max_length, null=True)
    last_name = models.CharField(max_length=max_length, null=True)

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

    # MBTI personality types
    mbti_choices = [
        ('INTJ', 'INTJ: The Architect'),
        ('INTP', 'INTP: The Logician'),
        ('ENTJ', 'ENTJ: The Commander'),
        ('ENTP', 'ENTP: The Visionary'),
        ('INFJ', 'INFJ: The Advocate'),
        ('INFP', 'INFP: The Idealist'),
        ('ENFJ', 'ENFJ: The Giver'),
        ('ENFP', 'ENFP: The Enthusiast'),
        ('ISTJ', 'ISTJ: The Duty Fulfiller'),
        ('ISFJ', 'ISFJ: The Protector'),
        ('ESTJ', 'ESTJ: The Executive'),
        ('ESFJ', 'ESFJ: The Caregiver'),
        ('ISTP', 'ISTP: The Craftsman'),
        ('ISFP', 'ISFP: The Artist')
    ]

    # Enneagram personality types
    enneagram_choices = [
        ('1', '1: The Reformer'),
        ('2', '2: The Helper'),
        ('3', '3: The Achiever'),
        ('4', '4: The Romantic'),
        ('5', '5: The Investigator'),
        ('6', '6: The Skeptic'),
        ('7', '7: The Enthusiast'),
        ('8', '8: The Challenger'),
        ('9', '9: The Peacemaker')
    ]

    mbti_personality = models.CharField(choices=mbti_choices, null=True)
    enneagram_personality = models.CharField(choices=enneagram_choices, null=True)

    # Long character description
    description = models.TextField(null=True)


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
