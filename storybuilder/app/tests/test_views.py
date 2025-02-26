from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser

from accounts.models import CustomUser
from app import views


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


    ### Teardown

    def tearDown(self):

        print("View Test Teardown")

        # Log out user from client
        self.client.logout()

        return super().tearDown()
