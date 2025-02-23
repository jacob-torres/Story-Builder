from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError

from accounts.models import CustomUser
from app.models import Story, Scene, Character, Plot, PlotPoint
from app.forms import *

# Create your tests here.
class StoryTestCase(TestCase):
    """Test case for the Story model."""

    def setUp(self):

        print("Story Model Test Setup")

        # Create new user object
        print("Creating new user object author1")
        self.author1 = CustomUser.objects.create(
            username='author1',
            email='author1@exampleemail.com',
            password='ILoveBooks123!',
            first_name='Alice',
            last_name='Writer'
        )

        # Create new story object
        print("Creating new story object story1")
        self.story1 = Story.objects.create(
            title='Story 1',
            description='Description for Story 1.',
            author_id=self.author1.id
        )

        return super().setUp()

    def test_story_create_and_update(self):
        """Test story creation and update."""

        print("*****************************")
        print("Testing Story Creation ...")

        # Run tests
        self.assertEqual(self.story1.title, 'Story 1')
        self.assertEqual(self.story1.description, 'Description for Story 1.')
        self.assertIsNone(self.story1.premise)
        self.assertEqual(self.story1.author_id, self.author1.id)
        self.assertEqual(Story.objects.count(), 1)

        # Add values to story
        print("Updating Story 1 with premise and genres")
        self.story1.premise = 'Premise for Story 1.'
        self.story1.genres = ['Fantasy', 'Horror', 'Experimental']
        self.story1.save()

        # Run tests for premise and genres
        self.assertIsNotNone(self.story1.premise)
        self.assertEqual(self.story1.premise, 'Premise for Story 1.')
        self.assertListEqual(self.story1.genres, ['Fantasy', 'Horror', 'Experimental'])
        self.assertIn('Horror', self.story1.genres)
        self.assertNotIn('', self.story1.genres)

        # Update story title
        print("Updating Story 1 title")
        self.story1.title = 'New Story Title'
        self.story1.save()

        # Run new story title tests
        self.assertNotEqual(self.story1.title, 'Story 1')
        self.assertEqual(self.story1.title, 'New Story Title')

    def test_valid_story_form(self):
        """Testing story creation and update with valid model form data."""

        print("*********************************")
        print("Testing valid story form Data")

        # Create story with model form
        print("Valid form data for Story 2")
        form_data = {
            'title': 'Story 2',
            'description': 'Description for Story 2.',
            'premise': 'Premise for Story 2.',
            'genres': ['Literary Fiction']
        }
        form = StoryForm(data=form_data, author_id=self.author1.id)
        story2 = form.save()

        # Run tests
        self.assertTrue(form.is_valid())
        self.assertIsInstance(story2, Story)
        self.assertEqual(story2.title, 'Story 2')

        # Update story via the model form
        print("Valid form data for updating Story 2")
        form_data['title'] = 'A Better Title'
        form = StoryForm(data=form_data, instance=story2)
        story2 = form.save()

        # Run tests for updated story
        self.assertTrue(form.is_valid())
        self.assertIsInstance(story2, Story)
        self.assertEqual(story2.title, 'A Better Title')

        # Delete new story object
        print("Deleting Story 2")
        story2.delete()
        self.assertFalse(Story.objects.filter(title='A Better Title').exists())

    def test_invalid_story_form(self):
        """Testing story creation and update with invalid model form data."""

        print("*****************************")
        print("Testing invalid story form data")

        # Create story with empty title
        print("Invalid form data with empty title")
        form_data = {
            'title': '',
            'description': 'Description for Story 1.',
        }
        form = StoryForm(data=form_data, author_id=self.author1.id)

        # Run tests for missing title
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

        # Create story with empty description
        print("Invalid form data with empty description")
        form_data = {
            'title': 'Story 2',
            'description': ''
        }
        form = StoryForm(data=form_data)

        # Run tests for missing description
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def tearDown(self):

        print("Story Model Test Teardown")

        # Delete story object and user object
        self.story1.delete()
        self.author1.delete()
        return super().tearDown()
