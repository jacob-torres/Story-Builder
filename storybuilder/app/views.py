from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404

from .forms import StoryForm, SceneForm, CharacterForm, PlotForm, PlotPointForm
from .models import Story, Scene, Character, Plot, PlotPoint

# Create your views here.
def home(request):
    """Home page."""
    return render(request, 'home.html')


# Story view functions
def stories(request):
    """View function for listing stories."""

    stories = Story.objects.all()
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
        form = StoryForm(request.POST)
        if form.is_valid():
            new_story = form.save()
            return redirect('story_detail', story_id=new_story.id)
    else:
        form = StoryForm()

    context = {'form': form}
    return render(request, 'new_story.html', context=context)


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


# View factory function
def view_factory(request, model_name, view_type, **kwargs):
    """A generic factory function for resolving view functions based on model."""

    try:
        model = None
        form = None
        template_name = ''
        context = {}

        match model_name:
            case 'story':
                model = Story
                form = StoryForm
            case 'character':
                model = Character
                form = CharacterForm
            case 'scene':
                model = Scene
                form = SceneForm
            case 'plot':
                model = Plot
                form = PlotForm
            case 'plot_point':
                model = PlotPoint
                form = PlotPointForm
            case _:
                raise ValueError(f"Invalid model name: {model_name}.")

        # Determine template name
        if view_type == 'detail':
            template_name = f"{model_name}_detail.html"
        elif view_type == 'create':
            template_name = f"new_{model_name}.html"
        elif view_type == 'update':
            template_name = f"update_{model_name}.html"
        elif view_type == 'DELETE':
            if model_name == 'story':
                template_name = 'stories.html'
            else:
                template_name = 'story_detail.html'
        else:
            raise ValueError(f"Invalid view type: {view_type}.")

        # Define ID args for specified objects
        story_id = kwargs.pop('story_id', None)
        character_id = kwargs.pop('character_id', None)
        scene_id = kwargs.pop('scene_id', None)
        plot_id = kwargs.pop('plot_id', None)
        plot_point_id = kwargs.pop('plot_point_id', None)

        # Ensure that the specified objects exist
        try:
            if story_id:
                story = get_object_or_404(Story, pk=story_id)
                print(f"story object {story_id} was found.")

            if character_id:
                character = get_object_or_404(Character, pk=character_id)
                print(f"Character object {character_id} was found.")

            if scene_id:
                scene = get_object_or_404(Scene, pk=scene_id)
                print(f"Scene object {scene_id} was found.")

            if plot_id:
                plot = get_object_or_404(Plot, pk=plot_id)
                print(f"Plot object {plot_id} was found.")

            if plot_point_id:
                plot_point = get_object_or_404(PlotPoint, pk=plot_point_id)
                print(f"Plot point object {plot_point_id} was found.")

        except Http404:
            return render(request, '404.html', status=404)

        # Determine view function
        if view_type == 'detail':
            if model == Story:
                context = {'story': story}
            else:
                context['story_title'] = story.title
                if model == Character:
                    context['character'] = character
                elif model == Scene:
                    context['scene'] = scene
                elif model_name == 'plot':
                    context['plot'] = plot
                elif model == PlotPoint:
                    context['plot_point'] = plot_point
        
        elif view_type == 'create':
            if request.method == 'POST':
                form = form(request.POST)
                if form.is_valid():
                    new_obj = form.save()

        return render(request=request, template_name=template_name, context=context)

    except ValueError as error:
        print("****************************************")
        print(error)
        return render(request, '500.html')