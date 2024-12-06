from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
# from django.views.generic.edit import UpdateView

from .forms import StoryForm, SceneForm, CharacterForm, PlotForm, PlotPointForm, WordCountForm, SceneNoteForm
from .models import Story, Scene, Character, Plot, PlotPoint

# Create your views here.
# class StoryWordCountUpdateView(UpdateView):
#     """Update view for the Story model."""

#     model = Story
#     fields = ['word_count']
#     form_class = WordCountForm
#     template_name = 'story_detail.html'

#     def get_context_data(self, **kwargs)    :
#         """Override get_context_data method for StoryUpdateView."""

#         print("**************************")
#         print("get_context_data in Story Update View")

#         context = super().get_context_data(**kwargs)
#         context['story'] = self.object
#         print(f"context: {context}")

#         return context

#     def form_valid(self, form):
#         """Override the form_valid method for the story update view."""

#         print("*********************************")
#         print("form_valid in story update view.")

#         self.object.word_count = form.cleaned_data['word_count']
#         self.object.save()
#         print(f"self.object: {self.object}")

#         return super().form_valid(form)


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
    print("Story Detail View")

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_id}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    # Instantiate word count update form
    if request.method == 'POST':
        form = WordCountForm(request.POST)
        if form.is_valid():
            story.word_count = form.cleaned_data['word_count']
            print(f"story.word_count: {story.word_count}")
            story.save()
    else:
        form = WordCountForm()

    context = {'story': story, 'form': form}
    print(f"context: {context}")

    return render(request, 'story_detail.html', context=context)


def create_or_update_story(request, story_id=None):
    """View function for creating a new story."""

    print("**************************************************")
    print("Create or Update Story View")

    template_name = ''
    context= {}

    try:
        # Update story if story ID is passed
        if story_id:
            print(f"Updating Story object {story_id}")

            try:
                story = get_object_or_404(Story, pk=story_id)
            except Http404:
                print(f"HTTP404 Error while getting Story object {story_id}.")
                print(error)
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
            print("Creating a new Story object ...")

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

    print(f"context: {context}")
    return render(request=request, template_name=template_name, context=context)


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
    """View function for rendering scene details."""

    print("*************************************")
    print("Scene Detail View")

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_id}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    try:
        scene = get_object_or_404(Scene, pk=scene_id)
    except Http404 as error:
        print(f"HTTP404 Error while getting Scene object {scene_id}.")
        print(error)
        return render(request, '404.html', status=404)

    # Add scene note form
    if request.method == 'POST':
        form = SceneNoteForm(request.POST)
        if form.is_valid() and form.cleaned_data['note'] not in scene.notes:
            print("Adding new scene note ...")
            print(form.cleaned_data['note'])
            scene.notes.append(form.cleaned_data['note'])
            scene.save()
    else:
        form = SceneNoteForm()

    context = {'story': story, 'scene': scene, 'form': form}
    print(f"context: {context}")

    return render(request, 'scene_detail.html', context=context)


def create_or_update_scene(request, story_id, scene_id=None):
    """View function for creating a new scene in a story."""

    print("******************************************")
    print("Create or Update Scene")

    template_name = ''
    context= {}

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_id}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    try:
        # Update scene
        if scene_id:
            print(f"Updating Scene object {scene_id}")

            if request.method == 'POST':
                form = SceneForm(request.POST, story_id=story_id, scene_id=scene_id)
                if form.is_valid():
                    scene = form.save()
                    return redirect('scene_detail', story_id=story_id, scene_id=scene_id)
            else:
                form = SceneForm(story_id=story_id, scene_id=scene_id)
                template_name = 'update_scene.html'
                context = {'form': form, 'story_title': story.title}

        # Create new scene
        else:
            print("Creating a new Scene object ...")

            if request.method == 'POST':
                form = SceneForm(request.POST, story_id=story_id)
                if form.is_valid():
                    new_scene = form.save()
                    return redirect('scene_detail', story_id=story_id, scene_id=new_scene.id)
            else:
                form = SceneForm(story_id=story_id)
                template_name = 'new_scene.html'
                context = {'form': form, 'story_title': story.title}

    except Exception as error:
        print("****** Error while creating or updating scene ******")
        print(error)
        template_name = '500.html'
        context = {'error': error}

    return render(request=request, template_name=template_name, context=context)


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


def create_or_update_character(request, story_id=None, character_id=None):
    """View function for creating a new character."""

    print("******************************************")
    print("Create or Update Character")

    template_name = ''
    context = {}

    try:
        story = get_object_or_404(Story, pk=story_id)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_id}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    try:
        # Update character
        if character_id:
            print(f"Updating Character object {character_id}")

            if request.method == 'POST':
                form = CharacterForm(request.POST, story_id=story_id, character_id=character_id)
                if form.is_valid():
                    character = form.save()
                    return redirect('character_detail', story_id=story_id, character_id=character_id)
            else:
                form = CharacterForm(story_id=story_id, character_id=character_id)
                template_name = 'update_character.html'
            context = {'form': form, 'story_title': story.title}

        # Create new character
        else:
            print("Creating a new Character object ...")

            if request.method == 'POST':
                form = CharacterForm(request.POST, story_id=story_id)
                if form.is_valid():
                    new_character = form.save()
                    return redirect('character_detail', story_id=story_id, character_id=new_character.id)
            else:
                form = CharacterForm(story_id=story_id)
                template_name = 'new_character.html'
            context = {'form': form, 'story_title': story.title}

    except Exception as error:
        print("****** Error while creating or updating character ******")
        print(error)
        template_name = '500.html'
        context = {'error': error}

    return render(request=request, template_name=template_name, context=context)


def delete_character(request, story_id, character_id):
    """View function for deleting a character."""

    try:
        story = get_object_or_404(Story, pk=story_id)
        character = get_object_or_404(Character, pk=character_id)
        character.delete()
    except Http404:
        return render(request, '404.html', status=404)

    return redirect('story_detail', story_id=story_id)
