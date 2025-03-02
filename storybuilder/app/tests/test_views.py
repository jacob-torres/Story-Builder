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

        # # Create story for testing scene functionality
        # print("Creating test story ...")
        # self.client.post(
        #     '/stories/new/',
        #     data={
        #         'title': 'Story 1',
        #         'description': 'A story for Testing!',
        #         'author_id': self.user.id
        #     }
        # )

        # Set up request factory for view function isolation
        self.request_factory = RequestFactory()

        return super().setUp()
    

    def test_view_home(self):
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


    def test_view_stories(self):
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

    def test_view_story_create_update(self):
        """Test for the create or update story view in creating a new story."""

        print("*****************************")
        print("Testing the view for creating and updating a story.")

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
            'description': 'Description for Story 2.',
            'author_id': self.user.id
        }
        response = self.client.post('/stories/new/', data=form_data)

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-2/')
        self.assertEqual(self.user.stories.count(), 2)

        # Test view function in isolation
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

        # Post request with view function in isolation
        print("New story view function with post request")
        form_data = {
            'title': 'Story 3',
            'description': 'Description for Story 3.',
            'author_id': self.user.id
        }

        request = self.request_factory.post('/stories/new/', data=form_data)
        request.user = self.user
        response = views.create_or_update_story(request)

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-3/')
        self.assertEqual(self.user.stories.count(), 3)

    def test_view_story_detail(self):
        """Test for the story detail view."""

        print("*********************************")
        print("Testing the story detail view")

        # Client request for story detail page
        print("Get request to the URL for story detail page")
        response = self.client.get('/stories/story-1/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Story 1 | The Story Builder</title>', response.content)
        self.assertIn(b'<h1>Story Details</h1>', response.content)
        self.assertIn(b'<h2>Description</h2>', response.content)

        # View function in isolation
        print("Story detail view function call with get request")
        request = self.request_factory.get('/stories/story-1/')
        request.user = self.user
        response = views.story_detail(request, story_slug='story-1')

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Story 1 | The Story Builder</title>', response.content)
        self.assertIn(b'<h1>Story Details</h1>', response.content)
        self.assertIn(b'<h2>Description</h2>', response.content)

    def test_view_scenes(self):
        """Test for the scenes view."""

        print("*******************************")
        print("Testing the scenes view")

        # Create a get request for the scenes URL
        print("Get request to the scenes URL")
        response = self.client.get('/stories/story-1/scenes/')

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'You have no scenes yet. When you do, they will be listed here.',
            response.content
        )

        # Test view function in isolation
        print("scenes view function call with get request")
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
        response = self.client.post(
            '/stories/story-1/scenes/new/',
            data=   {
                'title': 'Scene 1',
                'description': 'Description for Scene 1.'
            }
        )
        response = self.client.get('/stories/story-1/scenes/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<table>', response.content)
        self.assertIn(b'<th>Scene Title</th>', response.content)
        self.assertIn(b'<a href=1>Scene 1</a>', response.content)

    def test_view_scene_create_update(self):
        """Test for the create and update functionality for scenes."""

        print("**********************")
        print("Testing the view for creating and updating a scene.")

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
        response = self.client.post(
        '/stories/story-1/scenes/new/',
        data=   {
            'title': 'Scene 1',
            'description': 'Description for Scene 1.'
        }
    )

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
        response = self.client.post(
            '/stories/story-1/scenes/1/update/',
            data={
                'title': 'Scene 1',
                'description': 'Better description for Scene 1!'
            }
        )

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/stories/story-1/scenes/1/')
        self.assertEqual(
            self.story1.scene_set.get(order=1).description,
            'Better description for Scene 1!'
        )

        # Post request: update scene using the client with invalid data
        print("Post request to the update scene URL with empty title")
        response = self.client.post(
            '/stories/story-1/scenes/1/update/',
            data={
                'description': 'An even better description for Scene 1'
            }
        )

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIsNotNone(response.context['form'].errors)
        self.assertIn('title', response.context['form'].errors)

    def test_view_scene_detail(self):
        """Test for the scene detail page."""

    def test_view_scene_move(self):
        """Test for moving a scene up or down in the scene list."""

    def test_view_characters(self):
        """Test for the characters view."""

    def test_view_character_create_update(self):
        """Test for the create and update functionality for characters."""

    def test_view_character_detail(self):
        """Test for the character detail page."""
    
    def test_view_plot_create_update(self):
        """Test for the create and update functionality for the plot."""

    def test_view_plot_detail(self):
        """Test for the plot detail page."""

    def test_view_plotpoints(self):
        """Test for the plotpoints view."""

    def test_view_plotpoint_create_update(self):
        """Test for the create and update functionality for plot points."""

    def test_view_plotpoint_detail(self):
        """Test for the plot point detail page."""

    def test_view_plotpoint_move(self):
        """Test for moving a plot point up or down in the plot point list."""


    ### Teardown

    def tearDown(self):

        print("View Test Teardown")

        # Log out from client and delete user object
        self.client.logout()
        self.user.delete()

        return super().tearDown()
