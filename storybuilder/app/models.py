from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify

from accounts.models import CustomUser

from .constants import genre_choices, mbti_choices, enneagram_choices

# Length constants
tiny_length = 30
short_length = 100
mid_length = 250
long_length = 500


### Custom Story Manager

class StoryManager(models.Manager):
    """Custom manager for story objects."""

    def create(self, **kwargs):
        """
        An associated plot object is created and connected
        to each newly-created story object.
        """

        story = super().create(**kwargs)
        plot = Plot.objects.create(
            name=f"Plot for {story.title}",
            description=f"Description of the plot for {story.title}.",
            story_id=story.id
        )
        print(f"Successfully created new story {story.id} and plot {plot.id}.")
        return story


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
    slug = models.SlugField(max_length=mid_length, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name='stories')

    # Story object manager
    objects = StoryManager()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'title'],
                name='author_title_constraint'
            )
        ]

    def __str__(self):
        """Override the string method for the Story object."""
        return self.title
    
    def save(self, *args, **kwargs):
        """Override the save method for the story model."""
        self.slug = slugify(self.title)
        super(Story, self).save(*args, **kwargs)
    

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

    # Personality
    personality_traits = ArrayField(
        models.CharField(max_length=tiny_length),
        blank=True,
        null=True
    )
    mbti_personality = models.CharField(choices=mbti_choices, blank=True, null=True)
    enneagram_personality = models.CharField(choices=enneagram_choices, blank=True, null=True)

    # Long character description
    description = models.TextField(max_length=long_length, blank=True, null=True)

    story = models.ForeignKey(Story, on_delete=models.CASCADE, default=None)
    slug = models.SlugField(max_length=mid_length, blank=True)

    def __str__(self):
        """Override string method to display character name."""
        return self.full_name

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

    def save(self, *args, **kwargs):
        """Override the save method for the character model."""
        self.slug = slugify(self.full_name)
        super(Character, self).save(*args, **kwargs)


class Scene(models.Model):
    """A single unit or building block of a story."""

    title = models.CharField(max_length=short_length, null=False)
    description = models.TextField(max_length=long_length, null=True)
    notes = ArrayField(
        models.CharField(max_length=long_length),
        blank=True,
        default=list
    )

    # Relationships: One story and one possible plot point, one or more characters
    story = models.ForeignKey(Story, on_delete=models.CASCADE, default=None)
    plotpoint = models.ForeignKey('PlotPoint', on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    characters = models.ManyToManyField(Character, blank=True)

    # Order in display list
    order = models.SmallIntegerField(default=1, blank=True)

    def __str__(self):
        """Override the string method for the Scene object."""
        return self.title

    def save(self, *args, **kwargs):
        """Override the save method for the scene model."""

        if not self.id:
            prev_scene = Scene.objects.filter(
                story=self.story
            ).order_by('-order').first()
            if prev_scene:
                self.order = prev_scene.order + 1
        super().save(*args, **kwargs)


class Plot(models.Model):
    """Plots and their plot points, characters, and progressions."""

    name = models.CharField(max_length=short_length, null=False)
    description = models.TextField(max_length=long_length, null=True)
    story = models.OneToOneField(Story, on_delete=models.CASCADE, null=True, default=None, related_name='plot')

    def __str__(self):
        """Override the string method for the Plot object."""
        return self.name


class PlotPoint(models.Model):
    """A single point of a story's plot."""

    name = models.CharField(max_length=short_length, null=False)
    description = models.TextField(max_length=long_length, null=True)

    # Relationships: One plot
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, default=None)

    # Order in display list
    order = models.SmallIntegerField(default=1, blank=True)

    def __str__(self):
        """Override the string method for the PlotPoint object."""
        return self.name

    def save(self, *args, **kwargs):
        """Override the save method for the plot point model."""

        if not self.id:
            prev_point = PlotPoint.objects.filter(
                plot=self.plot
            ).order_by('-order').first()
            if prev_point:
                self.order = prev_point.order + 1
        super().save(*args, **kwargs)


class World(models.Model):
    """Worlds and their details."""

    name = models.CharField(max_length=short_length, null=False)
    description = models.TextField(max_length=long_length, null=True)

    # Relationships: One or more stories and characters
    stories = models.ManyToManyField(Story, blank=True)
    characters = models.ManyToManyField(Character, blank=True)

    def __str__(self):
        """Override the string method for the World object."""
        return self.name
