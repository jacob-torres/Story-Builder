from django.shortcuts import render
from django.http import HttpResponse
from .forms import NewStoryForm

# Create your views here.
def home(request):
    """Home page."""
    return render(request, 'home.html')


def stories(request):
    """View function for listing stories."""

    stories = []
    context = {'stories': stories}
    return render(request, 'stories.html', context=context)


def new_story(request):
    """View function for creating a new story."""

    if request.method == 'POST':
        form = NewStoryForm(request.POST)
        # ... form logic

    else:
        form = NewStoryForm()

    context = {'form': form}
    return render(request, 'new_story.html', context=context)
