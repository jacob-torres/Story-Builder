"""Utilities module for the Story Builder."""
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Story


def get_story_by_slug(story_slug):
    """Get a story object by a given URL slug."""

    try:
        story = get_object_or_404(Story, slug=story_slug)
        return story
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return None
