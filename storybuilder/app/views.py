from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .forms import NewStoryForm
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

    story = get_object_or_404(Story, pk=story_id)
    # if request.method == 'POST':
        # Update logic

    return render(request, 'update_story.html')


def delete_story(request, story_id):
    """View function for deleting a story."""

    story = get_object_or_404(Story, pk=story_id)
    story.delete()
    return redirect('stories')


def story_detail(request, story_id):
    """View function for displaying story details."""

    story = get_object_or_404(Story, pk=story_id)
    context = {'story': story}
    return render(request, 'story_detail.html', context=context)
