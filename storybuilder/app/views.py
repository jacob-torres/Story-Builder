from django.shortcuts import render, redirect
from django.db.models import F
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required

from .forms import StoryForm, SceneForm, CharacterForm, PlotForm, PlotPointForm, WordCountForm, SceneNoteForm, SceneCharacterForm
from .models import Story, Scene, Character, Plot, PlotPoint
from .utils import get_story_by_slug, get_scene, get_character, get_plot, get_plotpoint

# Create your views here.
def home(request):
    """View function for rendering the home page."""

    print("*****************************")
    print("Home Page")

    return render(request, 'home.html')


### Story view functions

@login_required
def stories(request):
    """View function for listing stories."""

    print("**********************************")
    print("Stories View")

    try:
        author_id = request.user.id
        stories = Story.objects.filter(author_id=author_id)
        context = {
            'stories': stories
        }
        return render(request, 'stories.html', context=context)
    except Exception as error:
        print("*********** Error while rendering story list ***********")
        print(error)
        return render(request, '500.html')


@login_required
def story_detail(request, story_slug):
    """View function for displaying story details."""

    print("\n**************************************************\n")
    print("Story Detail View\n")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)
    
    # Ordered scene list
    scenes = story.scene_set.all().order_by('order')

    # Get story plot
    plot = get_plot(story.id)
    if not plot:
        context = {'model_name': 'Plot'}
        return render(request, '404.html', status=404, context=context)

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

    context = {
        'story': story,
        'scenes': scenes,
        'plot': plot,
        'form': form
    }
    print(f"context: {context}")

    return render(request, 'story_detail.html', context=context)


@login_required
def create_or_update_story(request, story_slug=None):
    """View function for creating a new story."""

    print("**************************************************")
    print("Create or Update Story View")

    template_name = ''
    context= {}

    try:
        author_id = request.user.id

        # Update story if slug is passed
        if story_slug:
            story = get_story_by_slug(story_slug, author_id)
            if not story:
                context = {'model_name': 'Story'}
                return render(request, '404.html', status=404, context=context)

            if request.method == 'POST':
                print(f"Updating Story object {story_slug} ...")
                form = StoryForm(request.POST, instance=story)
                if form.is_valid():
                    story = form.save()
                    return redirect('story_detail', story_slug=story.slug)
            else:
                form = StoryForm(instance=story)

            template_name = 'update_story.html'
            context = {
                'form': form,
                'story_title': story.title
            }

        # Create story when no story slug is passed
        else:
            if request.method == 'POST':
                print("Creating a new Story object ...")
                form = StoryForm(request.POST, author_id=author_id)
                if form.is_valid():
                    try:
                        new_story = form.save()
                        new_plot = Plot.objects.create(
                            name=f"Plot for {new_story.title}",
                            description=f"Description of the plot for {new_story.title}.",
                            story_id=new_story.id
                        )
                        print(f"Successfully created new story {new_story.id} and plot {new_plot.id}.")
                        return redirect('story_detail', story_slug=new_story.slug)
                    except IntegrityError:
                        print("Duplicate story ...")
                        form.add_error(
                            None,
                            'You already have a story with this title.'
                        )
            else:
                form = StoryForm()

            # Default template name and context dictionary
            template_name = 'new_story.html'
            context = {
                'form': form
            }

    except Exception as error:
        print("****** Error while creating or updating story ******")
        print(error)
        return render(request, '500.html')

    try:
        print(f"context: {context}")
        return render(request=request, template_name=template_name, context=context)
    except Exception as error:
        print("*************** Error while rendering template ***************")
        print(error)
        return render(request, '500.html')


@login_required
def delete_story(request, story_slug):
    """View function for deleting a story."""

    print("*********************")
    print("Delete Story")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    try:
        story.delete()
    except Exception as error:
        print("There was an error while deleting the story.")
        print(error)

    return redirect('stories')


### Scene view functions

@login_required
def scenes(request, story_slug):
    """View function for listing scenes."""

    print("**********************************")
    print("Scenes View")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    try:
        scenes = Scene.objects.filter(story_id=story.id).order_by('order')
        context = {
            'story_title': story.title,
            'scenes': scenes
        }
        return render(request, 'scenes.html', context=context)
    except Exception as error:
        print("*********** Error while rendering scene list ***********")
        print(error)
        return render(request, '500.html')


@login_required
def scene_detail(request, story_slug, scene_order):
    """View function for rendering scene details."""

    print("*************************************")
    print("Scene Detail")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    scene = get_scene(story.id, scene_order)
    if not scene:
        context = {'model_name': 'Scene'}
        return render(request, '404.html', status=404, context=context)

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


@login_required
def create_or_update_scene(request, story_slug, scene_order=None):
    """View function for creating a new scene in a story."""

    print("******************************************")
    print("Create or Update Scene")

    template_name = ''
    context= {}

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    try:
        # Update scene
        if scene_order:
            scene = get_scene(story.id, scene_order)
            if not scene:
                context = {'model_name': 'Scene'}
                return render(request, '404.html', status=404, context=context)

            if request.method == 'POST':
                print(f"Updating Scene object {scene_order}")
                form = SceneForm(request.POST, instance=scene)
                if form.is_valid():
                    scene = form.save()
                    return redirect('scene_detail', story_slug=story_slug, scene_order=scene_order)

            else:
                form = SceneForm(instance=scene)

            template_name = 'update_scene.html'
            context = {
                'form': form,
                'story_title': story.title,
                'scene_title': scene.title
            }

        # Create new scene
        else:
            if request.method == 'POST':
                print("Creating a new Scene object ...")
                form = SceneForm(request.POST, story_id=story.id)
                if form.is_valid():
                    new_scene = form.save()
                    return redirect('scene_detail', story_slug=story_slug, scene_order=new_scene.order)

            else:
                # form = SceneForm(
                #     story_slug=story_slug,
                #     author_id=author_id
                # )
                form = SceneForm(story_id=story.id)

            template_name = 'new_scene.html'
            context = {
                'form': form,
                'story_title': story.title
            }

    except Exception as error:
        print("****** Error while creating or updating scene ******")
        print(error)
        return render(request, '500.html')

    try:
        print(f"context: {context}")
        return render(request=request, template_name=template_name, context=context)
    except Exception as error:
        print("*************** Error while rendering template ***************")
        print(error)
        return render(request, '500.html')


@login_required
def add_scene_character(request, story_slug: str, scene_order: int):
    """View function for the form for adding a character to a specific scene."""

    print("**********************")
    print("Add Scene Character")

    template_name = ''
    context = {}

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)
    
    scene = get_scene(story.id, scene_order)
    if not scene:
                context = {'model_name': 'Scene'}
                return render(request, '404.html', status=404, context=context)
    
    # Form logic for adding scene characters
    if request.method == 'POST':
        form = SceneCharacterForm(request.POST, instance=scene)
        if form.is_valid():
            scene = form.save()
            return redirect('scene_detail', story_slug=story_slug, scene_order=scene_order)
    else:
        form = SceneCharacterForm(instance=scene)

    template_name = 'add_scene_character.html'
    context = {
        'story_slug': story_slug,
        'story_title': story.title,
        'scene_title': scene.title,
        'form': form
    }

    print(f"context: {context}")
    return render(request=request, template_name=template_name, context=context)


@login_required
def delete_scene(request, story_slug, scene_order):
    """View function for deleting an existing scene in a story."""

    print("******************************")
    print("Delete Scene")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    scene = get_scene(story.id, scene_order)
    if not scene:
                context = {'model_name': 'Scene'}
                return render(request, '404.html', status=404, context=context)

    # Delete scene and update the order of the next scenes
    try:
        scene.delete()
        Scene.objects.filter(
            story=story,
            order__gt=scene_order
        ).update(order=F('order') - 1)

    except Exception as error:
        print("There was an error while deleting the scene.")
        print(error)

    return redirect('scenes', story_slug=story_slug)


### Character view functions

@login_required
def characters(request, story_slug):
    """View function for listing characters."""

    print("**********************************")
    print("Characters View")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    try:
        characters = Character.objects.filter(story_id=story.id)
        context = {
            'user': request.user,
            'story_title': story.title,
            'characters': characters
        }
        return render(request, 'characters.html', context=context)
    except Exception as error:
        print("*********** Error while rendering character list ***********")
        print(error)
        context = {'error': error}
        return render(request, '500.html')


@login_required
def character_detail(request, story_slug, character_slug):
    """View function for displaying character details."""

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    character = get_character(story.id, character_slug)
    if not character:
        context = {'model_name': 'Character'}
        return render(request, '404.html', status=404, context=context)

    context = {
        'story': story,
        'character': character
    }
    print(f"context: {context}")

    return render(request, 'character_detail.html', context=context)


@login_required
def create_or_update_character(request, story_slug=None, character_slug=None):
    """View function for creating a new character."""

    print("******************************************")
    print("Create or Update Character")

    template_name = ''
    context = {}

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    try:

        # Update character
        if character_slug:
            character = get_character(story.id, character_slug)

            if request.method == 'POST':
                print(f"Updating Character object {character_slug}")
                form = CharacterForm(request.POST, instance=character)
                if form.is_valid():
                    character = form.save(  )
                    return redirect('character_detail', story_slug=story_slug, character_slug=character.slug)
            else:
                form = CharacterForm(instance=character)

            template_name = 'update_character.html'
            context = {
                'form': form,
                'story_title': story.title
            }

        # Create new character
        else:
            if request.method == 'POST':
                print("Creating a new Character object ...")
                # form = CharacterForm(
                #     request.POST,
                #     story_slug=story_slug,
                #     author_id=author_id
                # )
                form = CharacterForm(request.POST, story_id=story.id)
                if form.is_valid():
                    new_character = form.save()
                    return redirect('character_detail', story_slug=story_slug, character_slug=new_character.slug)

            else:
                # form = CharacterForm(
                #     story_slug=story_slug,
                #     author_id=author_id
                # )
                form = CharacterForm(story_id=story.id)

            template_name = 'new_character.html'
            context = {
                'form': form,
                'story_title': story.title
            }

    except Exception as error:
        print("****** Error while creating or updating character ******")
        print(error)
        return render(request, '500.html')

    try:
        print(f"context: {context}")
        return render(request=request, template_name=template_name, context=context)
    except Exception as error:
        print("*************** Error while rendering template ***************")
        print(error)
        return render(request, '500.html')


@login_required
def delete_character(request, story_slug, character_slug):
    """View function for deleting a character."""

    print("**************************")
    print("Delete Character")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    character = get_character(story.id, character_slug)
    if not character:
        context = {'model_name': 'Character'}
        return render(request, '404.html', status=404, context=context)

    try:
        character.delete()
    except Exception as error:
        print("There was an error while deleting the character.")
        print(error)

    return redirect('characters', story_slug=story_slug)


### Plot View Functions

@login_required
def plot_detail(request, story_slug):
    """View function for rendering story plot details."""

    print("*************************************")
    print("Plot Details")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)
    
    # Get story plot
    plot = get_plot(story.id)
    if not plot:
        context = {'model_name': 'Plot'}
        return render(request, '404.html', status=404, context=context)

    context = {
        'story_title': story.title,
        'plot': plot
    }
    print(f"context: {context}")
    return render(request, 'plot_detail.html', context=context)


@login_required
def update_plot(request, story_slug):
    """View function for updating story plot details."""

    print("***********************************")
    print("Update Plot Details")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    # Get story plot
    plot = get_plot(story.id)
    if not plot:
        context = {'model_name': 'Plot'}
        return render(request, '404.html', status=404, context=context)
    
    if request.method == 'POST':
        form = PlotForm(request.POST, instance=plot)
        if form.is_valid():
            plot = form.save()
            return redirect('plot_detail', story_slug=story_slug)
    else:
        form = PlotForm(instance=plot)
    
    context = {
        'plot': plot,
        'form': form
    }
    print(f"context: {context}")
    return render(request, 'update_plot.html', context=context)


### Plot point view functions

@login_required
def plotpoint_detail(request, story_slug, plotpoint_order):
    """View function for rendering plot point details."""

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    plotpoint = get_plotpoint(story_slug, plotpoint_order)
    if not plotpoint:
        context = {'model_name': 'Plot Point'}
        return render(request, '404.html', status=404, context=context)
    
    context = {
        'story_slug': story.slug,
        'story_title': story.title,
        'plotpoint': plotpoint
    }

    return render(request, 'plotpoint_detail.html', context=context)


@login_required
def create_or_update_plotpoint(request, story_slug, plotpoint_order=None):
    """View function for creating or updating a plot point."""

    template_name = ''
    context = {}

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)
    
    # Define plot ID
    plot_id = story.plot.id
    print(f"plot ID: {plot_id}")

    # Update plot point
    if plotpoint_order:
        plotpoint = get_plotpoint(story_slug, plotpoint_order)
        if not plotpoint:
            context = {'model_name': 'Plot Point'}
            return render(request, '404.html', status=404, context=context)
        
        # Form logic
        if request.method == 'POST':
            print(f"Updating plot point {plotpoint_order} ...")
            form = PlotPointForm(
                request.POST,
                instance=plotpoint
            )
            if form.is_valid():
                plotpoint = form.save()
                return redirect(
                    'plotpoint_detail',
                    story_slug=story_slug,
                    plotpoint_order=plotpoint_order
                )

        else:
            form = PlotPointForm(instance=plotpoint)

        template_name = 'update_plotpoint.html'
        context = {
            'story_title': story.title,
            'plotpoint_order': plotpoint_order,
            'form': form
        }

    # Create new plot point
    else:
        print("Creating new plot point ...")

        if request.method == 'POST':
            print(f"Creating new plot point ...")
            form = PlotPointForm(request.POST, plot_id=plot_id)
            if form.is_valid():
                new_plotpoint = form.save()
                return redirect(
                    'plotpoint_detail',
                    story_slug=story_slug,
                    plotpoint_order=new_plotpoint.order
                )

        else:
            form = PlotPointForm(plot_id=plot_id)

        template_name = 'new_plotpoint.html'
        context = {
            'story_title': story.title,
            'form': form
        }

    return render(request=request, template_name=template_name, context=context)


@login_required
def delete_plotpoint(request, story_slug, plotpoint_order):
    """View function for deleting a plot point."""

    print("******************************")
    print("Delete Plot Point")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    plotpoint = get_plotpoint(story_slug, plotpoint_order)
    if not plotpoint:
        context = {'model_name': 'Plot Point'}
        return render(request, '404.html', status=404, context=context)

    # Delete plot point and update the order of the next plot points
    try:
        plot = plotpoint.plot
        plotpoint.delete()
        PlotPoint.objects.filter(
            plot=plot,
            order__gt=plotpoint_order
        ).update(order=F('order') - 1)
    except Exception as error:
        print("There was an error while deleting plot point.")
        print(error)

    return redirect('plot_detail', story_slug=story_slug)


### Vview functions to move scenes and plot points up or down in a list

@login_required
def move_up(request, story_slug, scene_order=None, plotpoint_order=None):
    """View function for moving scene or plot point objects up in a list."""

    print("******************")
    print("Move Up")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    if scene_order:
        print(f"Reordering scene {scene_order}")

        scene = get_scene(story.id, scene_order)
        if not scene:
                context = {'model_name': 'Scene'}
                return render(request, '404.html', status=404, context=context)
        
        print(f"Scene: {scene}")
        print(f"Scene order: {scene.order}")
        prev_scene = Scene.objects.filter(
            order__lt=scene.order,
            story=story
            ).order_by('-order').first()
        print(f"Previous scene: {prev_scene}")
        if prev_scene:
            print(f"Previous scene order: {prev_scene.order}")
            prev_scene.order, scene.order = scene.order, prev_scene.order
            prev_scene.save()
            scene.save()
            print(f"Successfully reordered scene to number {scene.order}")
        return redirect('scenes', story_slug=story_slug)

    elif plotpoint_order:
        print(f"Reordering plot point {plotpoint_order}")

        plotpoint = get_plotpoint(story_slug, plotpoint_order)
        if not plotpoint:
            context = {'model_name': 'Plot Point'}
            return render(request, '404.html', status=404, context=context)
        
        # FIXME: Get plot
        prev_plotpoint = PlotPoint.objects.filter(
            order__lt=plotpoint.order
            # plot=plot
        ).order_by('-order').first()
        if prev_plotpoint:
            prev_plotpoint.order, plotpoint.order = plotpoint.order, prev_plotpoint.order
            prev_plotpoint.save()
            plotpoint.save()
        return redirect('plot_detail', story_slug=story_slug)


@login_required
def move_down(request, story_slug, scene_order=None, plotpoint_order=None):
    """View function for moving scene or plot point objects down in a list."""

    print("******************")
    print("Move Down")

    author_id = request.user.id
    story = get_story_by_slug(story_slug, author_id)
    if not story:
        context = {'model_name': 'Story'}
        return render(request, '404.html', status=404, context=context)

    if scene_order:
        print(f"Reordering scene {scene_order}")

        scene = get_scene(story.id, scene_order)
        if not scene:
                context = {'model_name': 'Scene'}
                return render(request, '404.html', status=404, context=context)
        
        next_scene = Scene.objects.filter(order__gt=scene.order).order_by('order').first()
        if next_scene:
            next_scene.order, scene.order = scene.order, next_scene.order
            next_scene.save()
            scene.save()
        return redirect('story_detail', story_slug=story_slug)

    elif plotpoint_order:
        print(f"Reordering plot point {plotpoint_order}")

        plotpoint = get_plotpoint(story_slug, plotpoint_order)
        if not plotpoint:
            context = {'model_name': 'Plot Point'}
            return render(request, '404.html', status=404, context=context)
        
        next_plotpoint = PlotPoint.objects.filter(order__lt=plotpoint.order).order_by('-order').first()
        if next_plotpoint:
            next_plotpoint.order, plotpoint.order = plotpoint.order, next_plotpoint.order
            next_plotpoint.save()
            plotpoint.save()
        return redirect('plot_detail', story_slug=story_slug)
