from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    """Home page."""
    return render(request, 'home.html')


def stories(request):
    """View function for listing stories."""

    return render(request, 'stories.html')


def new_story(request):
    """View function for creating a new story."""

    return render(request, 'new_story.html')
