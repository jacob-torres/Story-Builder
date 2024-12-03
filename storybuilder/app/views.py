from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404

from .forms import StoryForm, SceneForm, CharacterForm, PlotForm, PlotPointForm
from .models import Story, Scene, Character, Plot, PlotPoint

# Create your views here.
def home(request):
    """Home page."""
    return render(request, 'home.html')


### Story view functions

def stories(request):
    """View function for listing stories."""

    stories = Story.objects.all()
    context = {'stories': stories}
    return render(request, 'stories.html', context=context)


def story_detail(request, story_id):
    """View function for displaying story details."""
    print("**************************************************")
    print("Create or Update Story View")

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404:
        return render(request, '404_story_not_found.html', status=404)

    # Manipulate genre values for proper template rendering
    # genres = story.genres.strip('[]').replace("'", "").replace("Childrens", "Children's")
    genres = story.genres
    print(f"story.genres: {story.genres}")
    print(type(story.genres))

    context = {'story': story, 'genres': genres}
    return render(request, 'story_detail.html', context=context)


def create_or_update_story(request, story_id=None):
    """View function for creating a new story."""

    template_name = ''
    context= {}

    try:
        # Update story if story ID is passed
        if story_id:
            try:
                story = get_object_or_404(Story, pk=story_id)
            except Http404:
                return render(request, '404_story_not_found.html', status=404)

            if request.method == 'POST':
                form = StoryForm(request.POST, instance=story)
                if form.is_valid():
                    story = form.save()
                    return redirect('story_detail', story_id=story.id)
            else:
                form = StoryForm(instance=story)
                template_name = 'update_story.html'
                context = {'form': form, 'story_title': story.title}

        # Create story when no story ID is passed
        else:
            if request.method == 'POST':
                form = StoryForm(request.POST)
                if form.is_valid():
                    new_story = form.save()
                    return redirect('story_detail', story_id=new_story.id)
            else:
                form = StoryForm()
                template_name = 'new_story.html'
                context = {'form': form}

    except Exception as error:
        print("****** Error while creating or updating story ******")
        print(error)
        template_name = '500.html'
        context = {'error': error}

    return render(request=request, template_name=template_name, context=context)


def update_story(request, story_id):
    """View function for updating a story."""

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404:
        return render(request, '404_story_not_found.html', status=404)

    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            story = form.save()
            return redirect('story_detail', story_id=story_id)
    else:
        form = StoryForm(instance=story)

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


# Scene view functions
# def scenes(request, story_id):
#     """View function for scenes URL, redirects to the story detail template."""

#     try:
#         story = get_object_or_404(Story, pk=story_id)
#     except Http404:
#         return render(request, '404_story_not_found.html', status=404)

    # context = {'story': story}
    # return render(request, 'story_detail.html', context=context)


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
        form = SceneForm(request.POST, story_id=story_id)
        if form.is_valid():
            new_scene = form.save()
            return redirect('scene_detail', story_id=story_id, scene_id=new_scene.id)
    else:
        form = SceneForm(story_id=story_id)

    context = {'form': form, 'story_title': story.title}
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

    return redirect('story_detail', story_id=story_id)


# Character view functions
def character_detail(request, story_id, character_id):
    """View function for displaying character details."""

    try:
        story = get_object_or_404(Story, pk=story_id)
        character = get_object_or_404(Character, pk=character_id)
    except Http404:
        return render(request, '404.html', status=404)

    context = {'story': story, 'character': character}
    return render(request, 'character_detail.html', context=context)


def new_character(request, story_id):
    """View function for creating a new character."""

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404:
        return render(request, '404_story_not_found.html', status=404)

    if request.method == 'POST':
        form = CharacterForm(request.POST, story_id=story_id)
        if form.is_valid():
            new_character = form.save()
            return redirect('character_detail', story_id=story_id, character_id=new_character.id)
    else:
        form = CharacterForm(story_id=story_id)

    context = {'form': form, 'story_title': story.title}
    return render(request, 'new_character.html', context=context)


def update_character(request, story_id, character_id):
    """View function for updating a character."""


def delete_character(request, story_id, character_id):
    """View function for deleting a character."""

