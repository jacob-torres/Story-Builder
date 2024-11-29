from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .forms import NewStoryForm, UpdateStoryForm
from .models import Story

# Create your views here.
def home(request):
    """Home page."""
    return render(request, 'home.html')


def stories(request):
    """View function for listing stories."""

    try:
        stories = get_list_or_404(Story)
    except:
        stories = []

    context = {'stories': stories}
    return render(request, 'stories.html', context=context)


def story_detail(request, story_id):
    """View function for displaying story details."""

    try:
        story = get_object_or_404(Story, pk=story_id)
    except:
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
    except:
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
    except:
        return render(request, '404_story_not_found.html', status=404)

    return redirect('stories')
