from django.test import TestCase
from django.urls import reverse
from django.db.utils import IntegrityError

from accounts.models import CustomUser
from app.models import Story, Scene, Character, Plot, PlotPoint
from app.forms import *

# Create your tests here.
class ModelTestCase(TestCase):
    """Test case for the Story model."""

    def setUp(self):

        print("Model Test Setup")

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


### Story Model Tests

    def test_story_model_create_update(self):
        """Test story creation and update."""

        print("*****************************")
        print("Testing Story Creation")

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

    def test_story_model_valid_form(self):
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

        # Create a story with a user-specified genre
        form_data = {
            'title': 'Story 3',
            'description': 'Description for Story 3.',
            'premise': 'Premise for Story 3.',
            'genres': ['Romance', 'Other'],
            'other_choice': 'A Wild New Genre'
        }
        form = StoryForm(data=form_data, author_id=self.author1.id)
        story3 = form.save()

        # Run test that other genre was properly handled in the clean method
        self.assertIn('A Wild New Genre', story3.genres)

        # Delete new story objects
        print("Deleting Story 2 and 3")
        story2.delete()
        story3.delete()

        # Test that Story 1 is the only story object left in the database
        self.assertEqual(Story.objects.count(), 1)

    def test_story_model_invalid_form(self):
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


    ### Scene Model Tests

    def test_scene_model_create_update(self):
        """Testing scene creation and update."""

        print("**************************")
        print("Testing Scene object creation and update")

        # Run initial tests before scene creation
        self.assertEqual(self.story1.scene_set.count(), 0)

        # Create new scene for Story 1
        print("Creating new scene for Story 1")
        scene1 = Scene.objects.create(
            title='Scene 1',
            description='Description for Scene 1 in Story 1.',
            story_id=self.story1.id
        )
        
        # Test scene creation
        self.assertNotEqual(self.story1.scene_set.count(), 0)
        self.assertTrue(
            Scene.objects.filter(title='Scene 1', story_id=self.story1.id).exists()
        )

        # Update scene data
        print("Update scene dataq")
        scene1.title = 'New Scene Title'
        scene1.save()

        # Test scene updated succesfully
        self.assertEqual(scene1.title, 'New Scene Title')
        self.assertEqual(self.story1.scene_set.count(), 1)

    def test_scene_modelvalid_form(self):
        """Test scene creation and update with valid form data."""

        print("*****************************")
        print("Testing scene creation and update with valid form data")

        # Valid form data
        print("Valid form data for creating a scene")
        form_data = {
            'title': 'Scene 2',
            'description': 'Description for Scene 2 in Story 1.'
        }
        form = SceneForm(data=form_data, story_id=self.story1.id)
        scene2 = form.save()

        # Test scene creation
        self.assertTrue(form.is_valid())
        self.assertTrue(
            Scene.objects.filter(title='Scene 2', story_id=self.story1.id).exists()
        )
        self.assertEqual(scene2.title, 'Scene 2')

        # Update scene data
        print("Update scene with invalid form data")
        form_data['description'] = 'A more exciting description!'
        form = SceneForm(data=form_data, instance=scene2)
        scene2 = form.save()

        # Test scene update
        self.assertTrue(form.is_valid())
        self.assertEqual(scene2.description, 'A more exciting description!')

        # Delete Scene 2
        print("Deleting Scene 2")
        scene2.delete()
        self.assertFalse(
            Scene.objects.filter(title='Scene 2').exists()
        )


    def test_scene_model_invalid_form(self):
        """Test for creating and updating scenes with invalid form data."""

        print("************************************")
        print("Testing scene creation and update with invalid form data")

        # Create scene
        print("Create scene with invalid form data")
        form_data = {
            'title': 'Scene 3',
            'description': ''
        }
        form = SceneForm(data=form_data, story_id=self.story1.id)

        # Test form validation
        self.assertFalse(form.is_valid())

        form_data['description'] = 'Valid description for Scene 3.'
        form = SceneForm(data=form_data, story_id=self.story1.id)
        scene3 = form.save()
        
        # Update scene data
        print("Update scene data with invalid form data")
        form_data['title'] = ''
        form = SceneForm(data=form_data, instance=scene3)

        # Test form validation
        self.assertFalse(form.is_valid())

        # Delete Scene 3
        print("Deleting Scene 3")
        scene3.delete()
        self.assertFalse(
            Scene.objects.filter(title='Scene 3').exists()
        )


    ### Teardown

    def tearDown(self):

        print("Model Test Teardown")

        # Delete story object and user object
        self.story1.delete()
        self.author1.delete()
        return super().tearDown()
