from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
from django.db.models import F

from .forms import StoryForm, SceneForm, CharacterForm, PlotForm, PlotPointForm, WordCountForm, SceneNoteForm
from .models import Story, Scene, Character, Plot, PlotPoint

# Create your views here.
def home(request):
    """Home page."""
    return render(request, 'home.html')


### Story view functions

def stories(request):
    """View function for listing stories."""

    try:
        stories = Story.objects.all()
        context = {'stories': stories}
        return render(request, 'stories.html', context=context)
    except Exception as error:
        print("*********** Error while rendering story list ***********")
        print(error)
        context = {'error': error}
        return render(request, '500.html', context=context)


def story_detail(request, story_slug):
    """View function for displaying story details."""

    print("**************************************************")
    print("Story Detail View")

    try:
        story = get_object_or_404(Story, slug=story_slug)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)
    
    # Ordered scene list
    scenes = story.scene_set.all().order_by('order')

    # Get story plot
    try:
        plot = get_object_or_404(Plot, story_id=story.id)
        print(f"plot ID: {plot.id}")
        print(f"plot points: {plot.plotpoint_set.all()}")
    except Exception as error:
        print("******* Error while getting story plot *******")
        print(error)
        return render(request, '404.html', status=404)

    # Instantiate word count update form
    if request.method == 'POST':
        form = WordCountForm(request.POST)
        if form.is_valid():
            story.word_count = form.cleaned_data['word_count']
            print(f"story.word_count: {story.word_count}")
            story.save()
            return redirect('story_detail', story_slug=story_slug)
    else:
        form = WordCountForm()

    context = {'story': story, 'scenes': scenes, 'plot': plot, 'form': form}
    # print(f"context: {context}")

    return render(request, 'story_detail.html', context=context)


def create_or_update_story(request, story_slug=None):
    """View function for creating a new story."""

    print("**************************************************")
    print("Create or Update Story View")

    template_name = ''
    context= {}

    try:
        # Update story if slug is passed
        if story_slug:

            try:
                story = get_object_or_404(Story, slug=story_slug)
            except Http404:
                print(f"HTTP404 Error while getting Story object {story_slug}.")
                print(error)
                return render(request, '404_story_not_found.html', status=404)

            if request.method == 'POST':
                print(f"Updating Story object {story_slug} ...")
                form = StoryForm(request.POST, instance=story)
                if form.is_valid():
                    story = form.save()
                    return redirect('story_detail', story_slug=story.slug)
            else:
                form = StoryForm(instance=story)
            template_name = 'update_story.html'
            context = {'form': form, 'story_title': story.title}

        # Create story when no story ID is passed
        else:
            if request.method == 'POST':
                print("Creating a new Story object ...")
                form = StoryForm(request.POST)
                if form.is_valid():
                    new_story = form.save()
                    new_plot = Plot.objects.create(
                        name=f"Plot for {new_story.title}",
                        description=f"Briefly summarize the plot of your story here.",
                        story_id=new_story.id
                    )
                    print(f"Successfully created new story {new_story.id} and plot {new_plot.id}.")
                    return redirect('story_detail', story_slug=new_story.slug)
            else:
                form = StoryForm()
            template_name = 'new_story.html'
            context = {'form': form}

    except Exception as error:
        print("****** Error while creating or updating story ******")
        print(error)
        template_name = '500.html'
        context = {'error': error}

    try:
        print(f"context: {context}")
        return render(request=request, template_name=template_name, context=context)
    except Exception as error:
        print("*************** Error while rendering template ***************")
        print(error)
        return render(request, '505.html', context={'error': error})


def delete_story(request, story_slug):
    """View function for deleting a story."""

    print("*********************")
    print("Delete Story View")

    try:
        story = get_object_or_404(Story, slug=story_slug)
        story.delete()
    except Http404 as error:
        print(f"HTTP404 Error while deleting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    return redirect('stories')


### Scene view functions

def scene_detail(request, story_slug, scene_order):
    """View function for rendering scene details."""

    print("*************************************")
    print("Scene Detail")

    try:
        story = get_object_or_404(Story, slug=story_slug)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    try:
        scene = get_object_or_404(Scene, story_id=story.id, order=scene_order)
    except Http404 as error:
        print(f"HTTP404 Error while getting Scene object {scene_order}.")
        print(error)
        return render(request, '404.html', status=404)

    # Add scene note form
    if request.method == 'POST':
        form = SceneNoteForm(request.POST)
        if form.is_valid():
            print("Adding new scene note ...")
            print(form.cleaned_data['note'])
            scene.notes.append(form.cleaned_data['note'])
            scene.save()
            return redirect('scene_detail', story_slug=story_slug, scene_order=scene_order)
    else:
        form = SceneNoteForm()

    context = {
        'scene': scene,
        'story_title': story.title,
        'story_slug': story.slug,
        'form': form
    }

    print(f"context: {context}")
    return render(request, 'scene_detail.html', context=context)


def create_or_update_scene(request, story_slug, scene_order=None):
    """View function for creating a new scene in a story."""

    print("******************************************")
    print("Create or Update Scene")

    template_name = ''
    context= {}

    try:
        story = get_object_or_404(Story, slug=story_slug)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    try:
        # Update scene
        if scene_order:

            try:
                scene = get_object_or_404(Scene, story_id=story.id, order=scene_order)
            except Http404 as error:
                print(f"HTTP404 Error while getting Scene object {scene_order}.")
                print(error)
                return render(request, '404.html', status=404)

            if request.method == 'POST':
                print(f"Updating Scene object {scene_order}")
                form = SceneForm(request.POST, story_slug=story_slug, instance=scene)
                if form.is_valid():
                    scene = form.save()
                    return redirect('scene_detail', story_slug=story_slug, scene_order=scene_order)
            else:
                form = SceneForm(story_slug=story_slug, instance=scene)
            template_name = 'update_scene.html'
            context = {'form': form, 'story_title': story.title}

        # Create new scene
        else:
            if request.method == 'POST':
                print("Creating a new Scene object ...")
                form = SceneForm(request.POST, story_slug=story_slug)
                if form.is_valid():
                    new_scene = form.save()
                    return redirect('scene_detail', story_slug=story_slug, scene_order=new_scene.order)
            else:
                form = SceneForm(story_slug=story_slug)
            template_name = 'new_scene.html'
            context = {'form': form, 'story_title': story.title}

    except Exception as error:
        print("****** Error while creating or updating scene ******")
        print(error)
        template_name = '500.html'
        context = {'error': error}

    try:
        print(f"context: {context}")
        return render(request=request, template_name=template_name, context=context)
    except Exception as error:
        print("*************** Error while rendering template ***************")
        print(error)
        return render(request, '505.html', context={'error': error})


def delete_scene(request, story_slug, scene_order):
    """View function for deleting an existing scene in a story."""

    print("******************************")
    print("Delete Scene")

    try:
        story = get_object_or_404(Story, slug=story_slug)
        scene = get_object_or_404(Scene, story_id=story.id, order=scene_order)
        scene.delete()

        # Update the order of the next scenes
        Scene.objects.filter(
            story=story,
            order__gt=scene_order
        ).update(order=F('order') - 1)

    except Http404 as error:
        print(f"HTTP404 Error while deleteing Scene object {scene_order}.")
        print(error)
        return render(request, '404.html', status=404)

    return redirect('story_detail', story_slug=story_slug)


### Character view functions

def character_detail(request, story_slug, character_slug):
    """View function for displaying character details."""

    try:
        story = get_object_or_404(Story, slug=story_slug)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)
    try:
        character = get_object_or_404(Character, slug=character_slug)
    except Http404 as error:
        print(f"HTTP404 Error while getting Character object {character_slug}.")
        print(error)
        return render(request, '404.html', status=404)

    context = {'story': story, 'character': character}
    print(f"context: {context}")

    return render(request, 'character_detail.html', context=context)


def create_or_update_character(request, story_slug=None, character_slug=None):
    """View function for creating a new character."""

    print("******************************************")
    print("Create or Update Character")

    template_name = ''
    context = {}

    try:
        story = get_object_or_404(Story, slug=story_slug)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    try:
        # Update character
        if character_slug:
            if request.method == 'POST':
                print(f"Updating Character object {character_slug}")
                form = CharacterForm(request.POST, story_slug=story_slug, character_slug=character_slug)
                if form.is_valid():
                    character = form.save()
                    return redirect('character_detail', story_slug=story_slug, character_slug=character_slug)
            else:
                form = CharacterForm(story_slug=story_slug, character_slug=character_slug)
            template_name = 'update_character.html'
            context = {'form': form, 'story_title': story.title}

        # Create new character
        else:
            if request.method == 'POST':
                print("Creating a new Character object ...")
                form = CharacterForm(request.POST, story_slug=story_slug)
                if form.is_valid():
                    new_character = form.save()
                    return redirect('character_detail', story_slug=story_slug, character_slug=new_character.slug)
            else:
                form = CharacterForm(story_slug=story_slug)
            template_name = 'new_character.html'
            context = {'form': form, 'story_title': story.title}

    except Exception as error:
        print("****** Error while creating or updating character ******")
        print(error)
        template_name = '500.html'
        context = {'error': error}

    try:
        print(f"context: {context}")
        return render(request=request, template_name=template_name, context=context)
    except Exception as error:
        print("*************** Error while rendering template ***************")
        print(error)
        return render(request, '505.html', context={'error': error})


def delete_character(request, story_slug, character_slug):
    """View function for deleting a character."""

    print("**************************")
    print("Delete Character")

    try:
        story = get_object_or_404(Story, slug=story_slug)
        character = get_object_or_404(Character, slug=character_slug)
        character.delete()
    except Http404 as error:
        print(f"HTTP404 Error while deleting Character object {character_slug}")
        print(error)
        return render(request, '404.html', status=404)

    return redirect('story_detail', story_slug=story_slug)


### Plot View Functions

def plot_detail(request, story_slug):
    """View function for rendering story plot details."""

    print("*************************************")
    print("Plot Details")

    try:
        story = get_object_or_404(Story, slug=story_slug)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)
    
    # Get story plot
    try:
        plot_id = story.plot.id
        plot = get_object_or_404(Plot, pk=plot_id)
    except Exception as error:
        print("******* Error while getting story plot *******")
        print(error)
        return render(request, '404.html', status=404)

    context = {'story_title': story.title, 'plot': plot}
    print(f"context: {context}")
    return render(request, 'plot_detail.html', context=context)


def update_plot(request, story_slug):
    """View function for updating story plot details."""

    print("***********************************")
    print("Update Plot Details")

    try:
        story = get_object_or_404(Story, slug=story_slug)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)
    
    # Get story plot
    try:
        plot_id = story.plot.id
        plot = get_object_or_404(Plot, pk=plot_id)
    except Exception as error:
        print("******* Error while getting story plot *******")
        print(error)
        return render(request, '404.html', status=404)
    
    if request.method == 'POST':
        form = PlotForm(request.POST, instance=plot)
        if form.is_valid():
            plot = form.save()
            return redirect('plot_detail', story_slug=story_slug)
    else:
        form = PlotForm(instance=plot)
    
    context = {'plot': plot, 'form': form}
    print(f"context: {context}")
    return render(request, 'update_plot.html', context=context)


### Plot point view functions

def plot_point_detail(request, story_slug, plot_point_order):
    """View function for rendering plot point details."""

    try:
        story = get_object_or_404(Story, slug=story_slug)
        plot_id = story.plot.id
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    try:
        plot_point = get_object_or_404(
            PlotPoint,
            plot_id=plot_id,
            order=plot_point_order
        )
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404.html', status=404)
    
    context = {
        'story_slug': story.slug,
        'story_title': story.title,
        'plot_point': plot_point
    }

    return render(request, 'plot_point_detail.html', context=context)


def create_or_update_plot_point(request, story_slug, plot_point_order=None):
    """View function for creating or updating a plot point."""

    template_name = ''
    context = {}

    try:
        story = get_object_or_404(Story, slug=story_slug)
        plot_id = story.plot.id
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    # Update plot point
    if plot_point_order:
        try:
            plot_point = get_object_or_404(
                PlotPoint,
                plot_id=plot_id,
                order=plot_point_order
            )
        except Http404 as error:
            print(f"HTTP404 Error while getting plot point object {plot_point_order}.")
            print(error)
            return render(request, '404.html', status=404)
        
        # Form logic
        if request.method == 'POST':
            print(f"Updating plot point {plot_point_order} ...")
            form = PlotPointForm(
                request.POST,
                story_slug=story_slug,
                plot_id=plot_id,
                instance=plot_point
            )
            if form.is_valid():
                plot_point = form.save()
                return redirect(
                    'plot_point_detail',
                    story_slug=story_slug,
                    plot_point_order=plot_point_order
                )

        else:
            form = PlotPointForm(
                story_slug=story_slug,
                plot_id=plot_id,
                instance=plot_point
            )

        template_name = 'update_plot_point.html'
        context = {
            'story_title': story.title,
            'plot_point_order': plot_point_order,
            'form': form
        }

    # Create new plot point
    else:
        print("Creating new plot point ...")

        if request.method == 'POST':
            print(f"Creating new plot point ...")
            form = PlotPointForm(
                request.POST,
                story_slug=story_slug,
                plot_id=plot_id
            )
            if form.is_valid():
                new_plot_point = form.save()
                return redirect(
                    'plot_point_detail',
                    story_slug=story_slug,
                    plot_point_order=new_plot_point.order
                )

        else:
            form = PlotPointForm(
                story_slug=story_slug,
                plot_id=plot_id
            )

        template_name = 'new_plot_point.html'
        context = {
            'story_title': story.title,
            'form': form
        }

    return render(request=request, template_name=template_name, context=context)


def delete_plot_point(request, story_slug, plot_point_order):
    """View function for deleting a plot point."""

    print("******************************")
    print("Delete Plot Point")

    try:
        story = get_object_or_404(Story, slug=story_slug)
        plot = story.plot
        plot_point = get_object_or_404(PlotPoint, plot_id=plot.id, order=plot_point_order)
        plot_point.delete()

        # Update the order of the next plot points
        PlotPoint.objects.filter(
            plot=plot,
            order__gt=plot_point_order
        ).update(order=F('order') - 1)

    except Http404 as error:
        print(f"HTTP404 Error while deleteing plot point object {plot_point_order}.")
        print(error)
        return render(request, '404.html', status=404)

    return redirect('plot_detail', story_slug=story_slug)


### Vview functions to move scenes and plot points up or down in a list

def move_up(request, story_slug, scene_order=None, plot_point_order=None):
    """View function for moving scene or plot point objects up in a list."""

    print("******************")
    print("Move Up")

    try:
        story = get_object_or_404(Story, slug=story_slug)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    if scene_order:
        print(f"Reordering scene {scene_order}")
        try:
            scene = get_object_or_404(Scene, story_id=story.id, order=scene_order)
        except Http404 as error:
            print(f"HTTP404 Error while getting Scene object {scene_order}.")
            print(error)
            return render(request, '404.html', status=404)
        
        prev_scene = Scene.objects.filter(order__lt=scene.order).order_by('-order').first()
        if prev_scene:
            prev_scene.order, scene.order = scene.order, prev_scene.order
            prev_scene.save()
            scene.save()
        return redirect('story_detail', story_slug=story_slug)

    elif plot_point_order:
        print(f"Reordering plot point {plot_point_order}")
        try:
            plot_point = get_object_or_404(PlotPoint, story_id=story.id, order=plot_point_order)
        except Http404 as error:
            print(f"HTTP404 Error while getting plot point object {plot_point_order}.")
            print(error)
            return render(request, '404.html', status=404)
        
        prev_plot_point = PlotPoint.objects.filter(order__lt=plot_point.order).order_by('-order').first()
        if prev_plot_point:
            prev_plot_point.order, plot_point.order = plot_point.order, prev_plot_point.order
            prev_plot_point.save()
            plot_point.save()
        return redirect('plot_detail', story_slug=story_slug)


def move_down(request, story_slug, scene_order=None, plot_point_order=None):
    """View function for moving scene or plot point objects down in a list."""

    print("******************")
    print("Move Down")

    try:
        story = get_object_or_404(Story, slug=story_slug)
    except Http404 as error:
        print(f"HTTP404 Error while getting Story object {story_slug}.")
        print(error)
        return render(request, '404_story_not_found.html', status=404)

    if scene_order:
        print(f"Reordering scene {scene_order}")
        try:
            scene = get_object_or_404(Scene, story_id=story.id, order=scene_order)
        except Http404 as error:
            print(f"HTTP404 Error while getting Scene object {scene_order}.")
            print(error)
            return render(request, '404.html', status=404)
        
        next_scene = Scene.objects.filter(order__gt=scene.order).order_by('order').first()
        if next_scene:
            next_scene.order, scene.order = scene.order, next_scene.order
            next_scene.save()
            scene.save()
        return redirect('story_detail', story_slug=story_slug)

    elif plot_point_order:
        print(f"Reordering plot point {plot_point_order}")
        try:
            plot_point = get_object_or_404(PlotPoint, story_id=story.id, order=plot_point_order)
        except Http404 as error:
            print(f"HTTP404 Error while getting plot point object {plot_point_order}.")
            print(error)
            return render(request, '404.html', status=404)
        
        next_plot_point = PlotPoint.objects.filter(order__lt=plot_point.order).order_by('-order').first()
        if next_plot_point:
            next_plot_point.order, plot_point.order = plot_point.order, next_plot_point.order
            next_plot_point.save()
            plot_point.save()
        return redirect('plot_detail', story_slug=story_slug)
