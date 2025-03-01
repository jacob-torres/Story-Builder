from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser

from accounts.models import CustomUser
from app import views, forms


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

        # Create client instance for sending URL requests
        self.client = Client()
        self.client.force_login(self.user)

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

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'You have no stories yet. When you do, they will be listed here.',
            response.content
        )

        # Test view function in isolation
        print("Stories view function call with get request")
        request = self.request_factory.get('/stories/')
        request.user = self.user
        response = views.stories(request)

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'You have no stories yet. When you do, they will be listed here.',
            response.content
        )

    def test_view_new_story(self):
        """Test for the create or update story view in creating a new story."""

        print("*****************************")
        print("Testing the story view for creating a new story.")

        # Connect using the client
        print("Get request to the new story URL")
        response = self.client.get('/stories/new/')

        # Test the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Create a New Story</h1>', response.content)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], forms.StoryForm)

        # Post request using the client
        print("Post request to the new story URL")
        form_data = {
            'title': 'Story 1',
            'description': 'Description for Story 1.',
            'author_id': self.user.id
        }
        response = self.client.post('/stories/new/', data=form_data)

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/stories/story-1/', response.url)
        self.assertEqual(self.user.stories.count(), 1)

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
            'title': 'Story 2',
            'description': 'Description for Story 2.',
            'author_id': self.user.id
        }

        request = self.request_factory.post('/stories/new/', data=form_data)
        request.user = self.user
        response = views.create_or_update_story(request)

        # Test the response
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/stories/story-2/', response.url)
        self.assertEqual(self.user.stories.count(), 2)

    def test_view_story_detail(self):
        """Test for the story detail view."""

        print("*********************************")
        print("Testing the story detail view")

        # Create new story for testing through the client
        print("Creating test story ...")
        self.client.post(
            '/stories/new/',
            data={
                'title': 'Story 1',
                'description': 'Description for Story 1.',
                'author_id': self.user.id
            }
        )

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


    ### Teardown

    def tearDown(self):

        print("View Test Teardown")

        # Log out from client and delete user object
        self.client.logout()
        self.user.delete()

        return super().tearDown()
