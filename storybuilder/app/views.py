from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404

from .forms import NewStoryForm, UpdateStoryForm, NewSceneForm
from .models import Story, Scene

# Create your views here.
def home(request):
    """Home page."""
    return render(request, 'home.html')


# Story view functions
def stories(request):
    """View function for listing stories."""

    try:
        stories = get_list_or_404(Story)
    except Http404:
        stories = []

    context = {'stories': stories}
    return render(request, 'stories.html', context=context)


def story_detail(request, story_id):
    """View function for displaying story details."""

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404:
        return render(request, '404_story_not_found.html', status=404)

    context = {'story': story}
    return render(request, 'story_detail.html', context=context)


def new_story(request):
    """View function for creating a new story."""

    if request.method == 'POST':
        form = NewStoryForm(request.POST)
        if form.is_valid():
            new_story = form.save()
            return redirect('story_detail', story_id=new_story.id)
    else:
        form = NewStoryForm()

    context = {'form': form}
    return render(request, 'new_story.html', context=context)


def update_story(request, story_id):
    """View function for updating a story."""

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404:
        return render(request, '404_story_not_found.html', status=404)

    if request.method == 'POST':
        form = UpdateStoryForm(request.POST, instance=story)
        if form.is_valid():
            story = form.save()
            return redirect('story_detail', story_id=story_id)
    else:
        form = UpdateStoryForm(instance=story)

    context = {'form': form, 'story': story}
    return render(request, 'update_story.html', context=context)


def delete_story(request, story_id):
    """View function for deleting a story."""

    try:
        story = get_object_or_404(Story, pk=story_id)
        story.delete()
    except Http404:
        return render(request, '404_story_not_found.html', status=404)

    return redirect('stories')


def scenes(request, story_id):
    """View function for listing all scenes in a story."""

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404:
        return render(request, '404_story_not_found.html', status=404)

    try:
        scenes = get_list_or_404(Scene)
    except Http404:
        scenes = []

    context = {'story': story, 'scenes': scenes}
    return render(request, 'scenes.html', context=context)


def scene_detail(request, story_id, scene_id):
    """View function for viewing scene details."""

    try:
        story = get_object_or_404(Story, pk=story_id)
        scene = get_object_or_404(Scene, pk=scene_id)
    except Http404:
        return render(request, '404.html', status=404)

    context = {'story': story, 'scene': scene}
    return render(request, 'scene_detail.html', context=context)


def new_scene(request, story_id):
    """View function for creating a new scene in a story."""

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404:
        return render(request, '404_story_not_found.html', status=404)

    if request.method == 'POST':
        form = NewSceneForm(request.POST)
        if form.is_valid():
            new_scene = form.save()
            new_scene.story = story
            new_scene.save()
            return redirect('scene_detail', story_id=story_id, scene_id=new_scene.id)
    else:
        form = NewSceneForm()

    context = {'form': form, 'story': story}
    return render(request, 'new_scene.html', context=context)


def update_scene(request, story_id, scene_id):
    """View function for updating an existing scene in a story."""

    try:
        story = get_object_or_404(Story, pk=story_id)
        scene = get_object_or_404(Scene, pk=scene_id)
    except Http404:
        return render(request, '404.html', status=404)

    # if request.method == 'POST':
    #     form = UpdateStoryForm(request.POST, instance=story)
    #     if form.is_valid():
    #         story = form.save()
    #         return redirect('story_detail', story_id=story_id)
    # else:
    #     form = UpdateStoryForm(instance=story)

    # context = {'form': form, 'story': story}
    # return render(request, 'update_story.html', context=context)


def delete_scene(request, story_id, scene_id):
    """View function for deleting an existing scene in a story."""

    try:
        story = get_object_or_404(Story, pk=story_id)
        scene = get_object_or_404(Scene, pk=scene_id)
        scene.delete()
    except Http404:
        return render(request, '404.html', status=404)

    return redirect('scenes', story_id=story_id)
