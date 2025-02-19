from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError

from accounts.models import CustomUser

from .models import Story, Scene, Character, Plot, PlotPoint
from.forms import *

# Create your tests here.
class StoryTestCase(TestCase):
    """Test case for the Story model."""

    def setUp(self):

        # Create new user object
        self.author1 = CustomUser.objects.create(
            username='author1',
            email='author1@exampleemail.com',
            password='ILoveBooks123!',
            first_name='Alice',
            last_name='Writer'
        )

        # Create new story object
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
        self.story1.title = 'New Story Title'
        self.story1.save()

        # Run new story title tests
        self.assertNotEqual(self.story1.title, 'Story 1')
        self.assertEqual(self.story1.title, 'New Story Title')

    def test_valid_story_form(self):
        """Testing story creation and update with valid model form data."""

        print("*********************************")
        print("Testing valid story form")

        # Create story with model form
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
        form_data['title'] = 'A Better Title'
        form = StoryForm(data=form_data, instance=story2)
        story2 = form.save()

        # Run tests for updated story
        self.assertTrue(form.is_valid())
        self.assertIsInstance(story2, Story)
        self.assertEqual(story2.title, 'A Better Title')

        # Delete new story object
        story2.delete()

    def test_invalid_story_form(self):
        """Testing story creation and update with invalid model form data."""

        # Create story with empty title
        form_data = {
            'title': '',
            'description': 'Description for Story 1.',
        }
        form = StoryForm(data=form_data, author_id=self.author1.id)

        # Run tests for missing title
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

        # Create story with empty description
        form_data = {
            'title': 'Story 2',
            'description': ''
        }
        form = StoryForm(data=form_data)

        # Run tests for missing description
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def tearDown(self):

        # Delete story object and user object
        self.story1.delete()
        self.author1.delete()
        return super().tearDown()
