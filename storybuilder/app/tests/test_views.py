from django.test import TestCase, Client

from accounts.models import CustomUser


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

        return super().setUp()
    

    def test_view_home_get(self):
        """Test for the home view function."""

        print("\n***********************\n")
        print("Testing the home view function\n")

        # Create get request for the home view
        print("Get request to the home view with no user logged in")
        response = self.client.get('/')

        # Test response status
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome to The Story Builder', response.content)

        # Create get request for the home view with user logged in
        print("Get request to the home view with user logged in")
        self.client.force_login(self.user)
        response = self.client.get('/')

        # Test status code
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome back, Jack!</h1>', response.content)

        # Log out user
        self.client.logout()


    ### Teardown

    def tearDown(self):

        print("View Test Teardown")

        # Log out user from client
        self.client.logout()

        return super().tearDown()
