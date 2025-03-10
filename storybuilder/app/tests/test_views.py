from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser

from accounts.models import CustomUser
from app import views, forms
from app.models import Story


class ViewTestCase(TestCase):
    """Test case for app view functions."""


    ### Setup

    def setUp(self):

        print("View Test Setup")

        # Create user object
        self.user = CustomUser.objects.create(
            username='writer5000',
            password='1VerySecurePassword!',
            email='example@email.com',
            first_name='Jack',
            last_name='Writer'
        )

        # Create story for testing story component functionality
        self.story1 = Story.objects.create(
            title='Story 1',
            description='Description for Story 1.',
            author_id=self.user.id
        )

        # Create client instance for sending URL requests
        self.client = Client()
        self.client.force_login(self.user)

        # Set up request factory for view function isolation
        self.request_factory = RequestFactory()

        return super().setUp()
    

    def test_home(self):
        """Test for the home view function."""

        print("***********************")
        print("Testing the home view function")

        # Create get request for the home view
        print("Get request to the home URL with no user logged in")
        self.client.logout()
        response = self.client.get('/')

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome to The Story Builder</h1>', response.content)

        # Create get request for the home view with user logged in
        print("Get request to the home URL with user logged in")
        self.client.force_login(self.user)
        response = self.client.get('/')

        # Test status code
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome back, Jack!</h1>', response.content)

        # Test view function in isolation
        print("Home view function call with no user logged in")
        request = self.request_factory.get('/')
        request.user = AnonymousUser()
        response = views.home(request)

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome to The Story Builder</h1>', response.content)

        # Request with user logged in
        print("Home view function call with user logged in")
        request.user = self.user
        response = views.home(request)

        # Test response status
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome back, Jack!</h1>', response.content)


    ### Story View Tests

    def test_stories(self):
        """Test for the stories view function."""

        print("*******************************")
        print("Testing the stories view")

        # Create a get request for the stories URL
        print("Get request to the stories URL")
        response = self.client.get('/stories/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table>', response.content)
        self.assertIn(b'<th>Story Title</th>', response.content)
        self.assertIn(b'<a href=story-1>Story 1</a>', response.content)

        # Test view function in isolation
        print("Stories view function call with get request")
        request = self.request_factory.get('/stories/')
        request.user = self.user
        response = views.stories(request)

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table>', response.content)
        self.assertIn(b'<th>Story Title</th>', response.content)
        self.assertIn(b'<a href=story-1>Story 1</a>', response.content)

        # Delete test story to test empty story list
        print("Get request to the stories URL with no stories")
        self.user.stories.all().delete()
        response = self.client.get('/stories/')

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'You have no stories yet. When you do, they will be listed here.',
            response.content
        )

        # Test view function in isolation
        print("Stories view function call with get request and no stories")
        request = self.request_factory.get('/stories/')
        request.user = self.user
        response = views.stories(request)

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'You have no stories yet. When you do, they will be listed here.',
            response.content
        )

    def test_story_create(self):
        """Test view functionality for creating a new story."""

        print("*****************************")
        print("Testing the view for creating a story.")

        # Get request: render new story form using the client
        print("Get request to the new story URL")
        response = self.client.get('/stories/new/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Create a New Story</h1>', response.content)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], forms.StoryForm)

        # Post request: create a story using the client
        print("Post request to the new story URL")
        form_data = {
            'title': 'Story 2',
            'description': 'Description for Story 2.'
        }
        response = self.client.post('/stories/new/', data=form_data)

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-2/')
        self.assertEqual(self.user.stories.count(), 2)

        # Post request: create a story using the client with invalid data
        print("Post request to the new story URL with empty title")
        form_data = {
            'title': '',
            'description': 'Description for invalid story.'
        }
        response = self.client.post('/stories/new/', data=form_data)

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIsNotNone(response.context['form'].errors)
        self.assertIn('title', response.context['form'].errors)
        self.assertEqual(self.user.stories.count(), 2)
        self.assertIn(b'<h1>Create a New Story</h1>', response.content)
        self.assertIn(b'<form method="post">', response.content)
        self.assertIn(b'<input type="text" name="title"', response.content)
        self.assertIn(b'<input type="checkbox" name="genres"', response.content)

        # Get request: view function call in isolation
        print("New story view function call with get request")
        request = self.request_factory.get('/stories/new/')
        request.user = self.user
        response = views.create_or_update_story(request)

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Create a New Story</h1>', response.content)
        self.assertIn(b'<form method="post">', response.content)
        self.assertIn(b'<input type="text" name="title"', response.content)
        self.assertIn(b'<input type="checkbox" name="genres"', response.content)

        # Post request: view function call in isolation
        print("New story view function with post request")
        form_data = {
            'title': 'Story 3',
            'description': 'Description for Story 3.'
        }

        request = self.request_factory.post('/stories/new/', data=form_data)
        request.user = self.user
        response = views.create_or_update_story(request)

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-3/')
        self.assertEqual(self.user.stories.count(), 3)

        # Post request: view function call in isolation with invalid data
        print("New story view function with post request and empty title")
        form_data = {
            'title': '',
            'description': 'Description for invalid story.'
        }

        request = self.request_factory.post('/stories/new/', data=form_data)
        request.user = self.user
        response = views.create_or_update_story(request)

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.stories.count(), 3)
        self.assertIn(b'<h1>Create a New Story</h1>', response.content)
        self.assertIn(b'<form method="post">', response.content)
        self.assertIn(b'<input type="text" name="title"', response.content)
        self.assertIn(b'<input type="checkbox" name="genres"', response.content)

    def test_story_update(self):

        # Get request: render the update story form using the client
        print("Get request to the update story URL")
        response = self.client.get('/stories/story-1/update/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'<title>Update Story 1 | The Story Builder</title>',
            response.content
        )
        self.assertIn(b'<h1>Update Story 1</h1>', response.content)
        self.assertIn(b'<form method="post">', response.content)
        self.assertIn(b'<input type="text" name="title"', response.content)
        self.assertIn(b'<input type="checkbox" name="genres"', response.content)

        # Post request: update a story using the client
        print("Post request to the update story URL")
        form_data = {
            'title': 'Better Title for Story 1',
            'description': 'Better description for Story 1!'
        }
        response = self.client.post('/stories/story-1/update/', data=form_data)

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/better-title-for-story-1/')
        self.assertTrue(
            self.user.stories.filter(description='Better description for Story 1!').exists()
        )
        self.assertFalse(
            self.user.stories.filter(title='Story 1').exists()
        )

        # Post request: update a story using the client with invalid form data
        print("Post request to the update story URL with empty title")
        form_data = {
            'title': '',
            'description': 'Better description for Story 1!'
        }
        response = self.client.post(
            '/stories/better-title-for-story-1/update/',
            data=form_data
        )

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIsNotNone(response.context['form'].errors)
        self.assertIn('title', response.context['form'].errors)

        # Get request: view function call in isolation for story update
        print("Update story view function call with get request")
        request = self.request_factory.get('/stories/story-1/update/')
        request.user = self.user
        response = views.create_or_update_story(request, story_slug='better-title-for-story-1')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Update Better Title for Story 1</h1>', response.content)
        self.assertIn(b'<form method="post">', response.content)
        self.assertIn(b'<input type="text" name="title"', response.content)
        self.assertIn(b'<input type="checkbox" name="genres"', response.content)

        # Post request: view function call in isolation for story update
        print("Update story view function with post request")
        form_data = {
            'title': 'New Story',
            'description': 'Description for new story.'
        }
        request = self.request_factory.post('/stories/story-1/update/', data=form_data)
        request.user = self.user
        response = views.create_or_update_story(
            request,
            story_slug='better-title-for-story-1'
        )

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/new-story/')
        self.assertTrue(
            self.user.stories.filter(title='New Story').exists()
        )
        self.assertFalse(
            self.user.stories.filter(title='Better Title for Story 1').exists()
        )

        # Post request: view function call in isolation for story update with invalid data
        print("Update story view function with post request and empty title")
        form_data = {
            'title': '',
            'description': 'Description for invalid story.'
        }

        request = self.request_factory.post('/stories/new-story/update/', data=form_data)
        request.user = self.user
        response = views.create_or_update_story(request, 'new-story')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            self.user.stories.filter(title='New Story').exists()
        )
        self.assertIn(b'<h1>Update New Story</h1>', response.content)
        self.assertIn(b'<form method="post">', response.content)
        self.assertIn(b'<input type="text" name="title"', response.content)
        self.assertIn(b'<input type="checkbox" name="genres"', response.content)

    def test_story_detail(self):
        """Test for the story detail view."""

        print("*********************************")
        print("Testing the story detail view")

        # Get request: render the story detail page using the client
        print("Get request to the URL for story detail page")
        response = self.client.get('/stories/story-1/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Story 1 | The Story Builder</title>', response.content)
        self.assertIn(b'<h1>Story Details</h1>', response.content)
        self.assertIn(b'<h2>Description</h2>', response.content)

        # Get request: story detail View function in isolation
        print("Story detail view function call with get request")
        request = self.request_factory.get('/stories/story-1/')
        request.user = self.user
        response = views.story_detail(request, story_slug='story-1')

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Story 1 | The Story Builder</title>', response.content)
        self.assertIn(b'<h1>Story Details</h1>', response.content)
        self.assertIn(b'<h2>Description</h2>', response.content)


    ### Scene View Tests

    def test_scenes(self):
        """Test for the scenes view."""

        print("*******************************")
        print("Testing the scenes view")

        # Get request: render the scenes page with no scenes using the client
        print("Get request to the scenes URL with no scenes")
        response = self.client.get('/stories/story-1/scenes/')

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'You have no scenes yet. When you do, they will be listed here.',
            response.content
        )

        # Get request: view function in isolation with no scenes
        print("scenes view function call with get request and no scenes")
        request = self.request_factory.get('/stories/story-1/scenes/')
        request.user = self.user
        response = views.scenes(request, story_slug='story-1')

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'You have no scenes yet. When you do, they will be listed here.',
            response.content
        )

        # Create a scene through the client for scene list testing
        print("Creating test scene ...")
        form_data = {
            'title': 'Scene 1',
            'description': 'Description for Scene 1.'
        }
        response = self.client.post('/stories/story-1/scenes/new/', data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/scenes/1/')

        # Get request: Render the scenes page with 1 scene using the client
        print("Get request to the scenes URL with 1 scene")
        response = self.client.get('/stories/story-1/scenes/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table>', response.content)
        self.assertIn(b'<th>Scene Title</th>', response.content)
        self.assertIn(b'<a href=1>Scene 1</a>', response.content)

        # Get request: scenes view function in isolation with 1 scene
        print("Scenes view function call with get request and 1 scene")
        request = self.request_factory.get('/stories/story-1/scenes/')
        request.user = self.user
        response = views.scenes(request, story_slug='story-1')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table>', response.content)
        self.assertIn(b'<th>Scene Title</th>', response.content)
        self.assertIn(b'<a href=1>Scene 1</a>', response.content)

    def test_scene_create(self):
        """Test for the view functionality for creating scenes."""

        print("**********************")
        print("Testing the view for creating a scene.")

        # Get request: render new scene form using the client
        print("Get request to the new scene URL")
        response = self.client.get('/stories/story-1/scenes/new/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Create a New Scene in Story 1</h1>', response.content)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], forms.SceneForm)

        # Post request: Create a scene using the client
        print("Post request to the new scene URL")
        form_data = {
            'title': 'Scene 1',
            'description': 'Description for Scene 1.'
        }
        response = self.client.post('/stories/story-1/scenes/new/', data=form_data)

    # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/scenes/1/')
        self.assertEqual(self.story1.scene_set.count(), 1)

        # Post request: Create a scene using the client with invalid data
        print("Post request to the new scene URL with empty title")
        response = self.client.post(
        '/stories/story-1/scenes/new/',
        data=   {
            'description': 'Description for invalid scene.'
        }
    )

    # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIsNotNone(response.context['form'].errors)
        self.assertIn('title', response.context['form'].errors)
        self.assertEqual(self.story1.scene_set.count(), 1)

    def test_scene_update(self):
        """Test for the view functionality for updating scenes."""

        print("**********************")
        print("Testing the view for updating a scene.")

        # Create scene for update testing
        form_data = {
            'title': 'Scene 1',
            'description': 'Description for Scene 1.'
        }
        response = self.client.post('/stories/story-1/scenes/new/', data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/scenes/1/')

        # Get request: render update scene form using the client
        print("Get request to the update scene URL")
        response = self.client.get('/stories/story-1/scenes/1/update/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'<h1>Update Scene Scene 1 from Story 1</h1>',
            response.content
        )
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], forms.SceneForm)

        # Post request: update scene using the client
        print("Post request to the update scene URL")
        form_data = {
            'title': 'Scene 1',
            'description': 'Better description for Scene 1!'
        }
        response = self.client.post('/stories/story-1/scenes/1/update/', data=form_data)

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/scenes/1/')
        self.assertEqual(
            self.story1.scene_set.get(order=1).description,
            'Better description for Scene 1!'
        )

        # Post request: update scene using the client with invalid data
        print("Post request to the update scene URL with empty title")
        form_data = {
            'description': 'An even better description for Scene 1'
        }
        response = self.client.post('/stories/story-1/scenes/1/update/', data=form_data)

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIsNotNone(response.context['form'].errors)
        self.assertIn('title', response.context['form'].errors)

    def test_scene_detail(self):
        """Test for the scene detail page."""

        print("**********************")
        print("Testing the scene detail page.")

        # Create test scene
        form_data = {
            'title': 'Scene 1',
            'description': 'Description for Scene 1.'
            }
        response = self.client.post('/stories/story-1/scenes/new/', data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/scenes/1/')

        # Get request: render scene detail page using the client
        print("Get request to the scene detail URL")
        response = self.client.get('/stories/story-1/scenes/1/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn(
            b'<form id="scene-note-form" style="display: none;" method="post">',
            response.content
        )
        self.assertIn(b'<h1>Scene 1</h1>', response.content)
        self.assertIn   (
            b'<h2>Scene Number 1 in <a href="/stories/story-1">Story 1</a></h2>',
            response.content
        )
        self.assertIn(
            b'<p>Description for Scene 1.</p>',
            response.content
        )

        # Get request: scene detail view function in isolation
        print("Scene detail view function call with get request")
        request = self.request_factory.get('/stories/story-1/scenes/1/')
        request.user = self.user
        response = views.scene_detail(request, story_slug='story-1', scene_order=1)

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Scene 1, from Story 1 | The Story Builder</title>', response.content)
        self.assertIn(b'<h1>Scene 1</h1>', response.content)
        self.assertIn(
            b'<h2>Scene Number 1 in <a href="/stories/story-1">Story 1</a></h2>',
            response.content
        )
        self.assertIn(b'<p>Description for Scene 1.</p>', response.content)

    def test_scene_move(self):
        """Test for moving a scene up or down in the scene list."""

        print("***************************")
        print("Testing the view functionality for moving a scene up or down in the list")

        # Create test scenes
        print("Creating test scenes ...")
        for i in range(1, 4):
            form_data = {'title': f'Scene {i}'}
            response = self.client.post('/stories/story-1/scenes/new/', data=form_data)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, f'/stories/story-1/scenes/{i}/')
        self.assertEqual(self.story1.scene_set.count(), 3)

        # Get request: render the scenes page after moving a scene up using the client
        print("Get request to the scenes URL after moving a scene up")
        response = self.client.get('/stories/story-1/scenes/2/up/')

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/scenes/')
        self.assertEqual(
            self.story1.scene_set.get(title='Scene 2').order, 1
        )
        self.assertEqual(
            self.story1.scene_set.get(title='Scene 1').order, 2
        )

        # Get request: view function for moving a scene up in isolation
        print("View function call for moving a scene up")
        request = self.request_factory.get('/stories/story-1/scenes/3/up/')
        request.user = self.user
        response = views.move_up(request, story_slug='story-1', scene_order=3)

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/scenes/')
        self.assertEqual(
            self.story1.scene_set.get(title='Scene 3').order, 2
        )
        self.assertEqual(
            self.story1.scene_set.get(title='Scene 1').order, 3
        )

        # Get request: render the scenes page after moving a scene down using the client
        print("Get request to the scenes URL after moving a scene down")
        response = self.client.get('/stories/story-1/scenes/2/down/')

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/scenes/')
        self.assertEqual(
            self.story1.scene_set.get(title='Scene 3').order, 3
        )
        self.assertEqual(
            self.story1.scene_set.get(title='Scene 1').order, 2
        )

        # Get request: view function for moving a scene down in isolation
        print("View function call for moving a scene down")
        request = self.request_factory.get('/stories/story-1/scenes/1/down/')
        request.user = self.user
        response = views.move_down(request, story_slug='story-1', scene_order=1)

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/scenes/')
        self.assertEqual(
            self.story1.scene_set.get(title='Scene 2').order, 2
        )
        self.assertEqual(
            self.story1.scene_set.get(title='Scene 1').order, 1
        )


    ### Character View Tests

    def test_characters(self):
        """Test for the characters view."""

        print("*******************************")
        print("Testing the characters view")

        # Get request: render the characters page with no characters using the client
        print("Get request to the characters URL with no characters")
        response = self.client.get('/stories/story-1/characters/')

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'There are no characters in this story yet. When you add some, they will be listed here.',
            response.content
        )

        # Get request: view function in isolation with no characters
        print("characters view function call with get request and no characters")
        request = self.request_factory.get('/stories/story-1/characters/')
        request.user = self.user
        response = views.characters(request, story_slug='story-1')

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'There are no characters in this story yet. When you add some, they will be listed here.',
            response.content
        )

        # Create a character through the client for character list testing
        print("Creating test character ...")
        form_data = {'first_name': 'Alice'}
        response = self.client.post('/stories/story-1/characters/new/', data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/characters/alice/')

        # Get request: Render the characters page with 1 scene using the client
        print("Get request to the characters URL with 1 character")
        response = self.client.get('/stories/story-1/characters/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table>', response.content)
        self.assertIn(b'<th>Name</th>', response.content)
        self.assertIn(b'<a href=alice>Alice</a>', response.content)

        # Get request: characters view function in isolation with 1 scene
        print("characters view function call with get request and 1 character")
        request = self.request_factory.get('/stories/story-1/characters/')
        request.user = self.user
        response = views.characters(request, story_slug='story-1')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table>', response.content)
        self.assertIn(b'<th>Name</th>', response.content)
        self.assertIn(b'<a href=alice>Alice</a>', response.content)

    def test_character_create(self):
        """Test for the view functionality for creating characters."""

        print("**********************")
        print("Testing the view for creating a character.")

        # Get request: render new character form using the client
        print("Get request to the new character URL")
        response = self.client.get('/stories/story-1/characters/new/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Create a New Character in Story 1</h1>', response.content)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], forms.CharacterForm)

        # Post request: Create a character using the client
        print("Post request to the new character URL")
        form_data = {
            'first_name': 'Alice',
            'location': 'Wonderland',
            'description': 'Alice is a curious girl.'
        }
        response = self.client.post('/stories/story-1/characters/new/', data=form_data)

    # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/characters/alice/')
        self.assertEqual(self.story1.character_set.count(), 1)
        self.assertEqual(
            self.story1.character_set.get(first_name='Alice').location,
            'Wonderland'
        )

        # Post request: Create a character using the client with invalid data
        print("Post request to the new character URL with empty first name")
        form_data = {
            'last_name': 'Lastname',
            'description': 'Description for invalid character.'
        }
        response = self.client.post('/stories/story-1/characters/new/', data=form_data)

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIsNotNone(response.context['form'].errors)
        self.assertIn('first_name', response.context['form'].errors)
        self.assertEqual(self.story1.character_set.count(), 1)

    def test_character_update(self):
        """Test for the view functionality for updating characters."""

    def test_character_detail(self):
        """Test for the character detail page."""


    ### Plot Point View Tests

    def test_plot_create(self):
        """Test for the view functionality for automatic plot creation."""

    def test_plot_update(self):
        """Test for the view functionality for updating a plot."""

    def test_plot_detail(self):
        """Test for the plot detail page and plot point list."""


    ### Plot Point View Tests

    def test_plotpoint_create(self):
        """Test for the view functionality for creating plot points."""

    def test_plotpoint_update(self):
        """Test for the view functionality for updating plot points."""

    def test_plotpoint_detail(self):
        """Test for the plot point detail page."""

    def test_plotpoint_move(self):
        """Test for moving a plot point up or down in the plot point list."""


    ### Teardown

    def tearDown(self):

        print("View Test Teardown")

        # Log out from client and delete user object
        self.client.logout()
        self.user.delete()

        return super().tearDown()
