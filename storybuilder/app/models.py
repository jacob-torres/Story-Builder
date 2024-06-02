import uuid
from django.db import models

# Create your models here.
class Story(models.Model):
    """A collection of ideas."""

    story_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_column='story_id',
        editable=False
    )

    story_rank = models.AutoField(
        default=0,
        db_column='story_rank',
        unique=True
    )

    story_title = models.CharField(
        max_length=250,
        default='Story Title',
        db_column='story_title',
        help_text='Enter your story title.'
    )

    story_ideas = models.JSONField(
        db_column='story_ideas',
        null=True,
        help_text='The list of ideas which make up your story.'
    )


class Idea(models.Model):
    """The smallest unit of a story.
    
    An idea can be composed of text, an image, and a list of reference links.
    """

    idea_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_column='idea_id',
        editable=False
    )

    idea_story = models.ForeignKey(to=Story, on_delete=models.CASCADE)

    idea_rank = models.AutoField(
        default=0,
        db_column='idea_rank',
        unique=True
    )

    idea_description = models.CharField(
        max_length=500,
        default='Idea Description',
        db_column='idea_description',
        help_text='Write a brief description of your idea.'
    )

    idea_text = models.TextField(
        default='Idea Text',
        db_column='idea_text',
        help_text='Write anything you want to about your idea.'
    )

    idea_image = models.ImageField(
        db_column='idea_image',
        null=True,
        help_text='Upload an image to visualize your idea.'
    )

    idea_links = models.JSONField(
        db_column='idea_links',
        null=True,
        help_text='A list of links to your idea references.'
    )