"""Utilities module for the Story Builder."""
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Story, Scene, Character, Plot, PlotPoint


def get_story_by_slug(story_slug: str, author_id: int):
    """Get a story object by a given URL slug."""

    try:
        story = get_object_or_404(Story, slug=story_slug, author_id=author_id)
        return story
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return None


def get_scene(story_id: int, scene_order: int):
    """Get a scene object by story ID and scene order."""

    try:
        scene = get_object_or_404(
            Scene,
            story_id=story_id,
            order=scene_order
        )
        return scene

    except Http404 as error:
        print(f"HTTP404 Error while getting Scene object {scene_order}.")
        print(error)
        return None


def get_character(story_id: int, character_slug: str):
    """Get a character object by story ID and character slug."""

    try:
        character = get_object_or_404(
            Character,
            story_id=story_id,
            slug=character_slug
        )
        return character

    except Http404 as error:
        print(f"HTTP404 Error while getting character object {character_slug}.")
        print(error)
        return None


def get_plot(story_id: int):
    """Get a plot object by its associated story object."""

    try:
        plot = get_object_or_404(Plot, story_id=story_id)
        return plot

    except Http404 as error:
        print(f"HTTP404 Error while getting plot object for story ID {story_id}.")
        print(error)
        return None


def get_plotpoint(story_slug: str, plotpoint_order: int):
    """Get a plot point object by story ID and plot point order."""

    story = get_story_by_slug(story_slug)
    if not story:
        return None

    try:
        plot_id = story.plot.id
        plotpoint = get_object_or_404(
            PlotPoint,
            plot_id=plot_id,
            order=plotpoint_order
        )
        return plotpoint

    except Http404 as error:
        print(f"HTTP404 Error while getting plot point object {plotpoint_order}.")
        print(error)
        return None
