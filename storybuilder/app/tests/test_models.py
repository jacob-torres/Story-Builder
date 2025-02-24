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
        print("Invalid form data for creating a story with an empty title")
        form_data = {
            'title': '',
            'description': 'Description for Story 1.',
        }
        form = StoryForm(data=form_data, author_id=self.author1.id)

        # Run tests for missing title
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

        # Create story with empty description
        print("Invalid form data for creating a story with an empty description")
        form_data = {
            'title': 'Story 2',
            'description': ''
        }
        form = StoryForm(data=form_data)

        # Run tests for missing description
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

        # Create valid story for testing update functionality
        print("Valid form data for updating a story")
        form_data = {
            'title': 'Valid Story Title',
            'description': 'Valid story description.'
        }
        form = StoryForm(data=form_data, author_id=self.author1.id)
        story2 = form.save()

        # Update story
        print("Invalid form data for updating a story with an empty description")
        form_data['description'] = ''
        form = StoryForm(data=form_data, instance=story2)

        # Test update with empty description
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

        # Test scene update
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
        self.assertIsInstance(scene2, Scene)
        self.assertTrue(
            Scene.objects.filter(title='Scene 2', story_id=self.story1.id).exists()
        )
        self.assertEqual(scene2.title, 'Scene 2')
        self.assertEqual(self.story1.scene_set.count(), 1)

        # Update scene data
        print("Valid form data for updating a scene")
        form_data['description'] = 'A more exciting description!'
        form = SceneForm(data=form_data, instance=scene2)
        scene2 = form.save()

        # Test scene update
        self.assertTrue(form.is_valid())
        self.assertEqual(scene2.description, 'A more exciting description!')

        # Delete Scene 2
        print("Deleting Scene 2")
        scene2.delete()

        # Test scene deletion
        self.assertFalse(
            Scene.objects.filter(title='Scene 2').exists()
        )
        self.assertEqual(self.story1.scene_set.count(), 0)


    def test_scene_model_invalid_form(self):
        """Test for creating and updating scenes with invalid form data."""

        print("************************************")
        print("Testing scene creation and update with invalid form data")

        # Create scene
        print("Invalid form data for creating a scene with an empty description")
        form_data = {
            'title': 'Scene 3',
            'description': ''
        }
        form = SceneForm(data=form_data, story_id=self.story1.id)

        # Test form validation
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

        # Create valid scene for testing update functionality
        form_data['description'] = 'Valid description for Scene 3.'
        form = SceneForm(data=form_data, story_id=self.story1.id)
        scene3 = form.save()
        
        # Update scene data
        print("Invalid form data for updating a scene with an empty title")
        form_data['title'] = ''
        form = SceneForm(data=form_data, instance=scene3)

        # Test form validation
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

        # Delete Scene 3
        print("Deleting Scene 3")
        scene3.delete()

        # Test scene deletion
        self.assertFalse(
            Scene.objects.filter(title='Scene 3').exists()
        )
        self.assertEqual(self.story1.scene_set.count(), 0)


    ### Character Tests

    def test_character_model_create_update(self):
        """Test for character creation and update."""

        print("***************************")
        print("Testing character creation and update")

        # Create character
        print("Create character for Story 1")
        character1 = Character.objects.create(first_name='Bob', story_id=self.story1.id)

        # Test character creation
        self.assertEqual(character1.first_name, 'Bob')
        self.assertIsInstance(character1, Character)
        self.assertEqual(Character.objects.count(), 1)
        self.assertTrue(
            Character.objects.filter(first_name='Bob', story_id=self.story1.id).exists()
        )

        # Test character update
        character1.first_name = 'Alice'
        character1.location = 'Wonderland'
        character1.save()

        # Test character update
        self.assertEqual(character1.first_name, 'Alice')
        self.assertEqual(character1.location, 'Wonderland')

    def test_character_model_valid_form(self):
        """Test for character creation and update with valid form data."""

        print("****************************")
        print("Testing character creation and update with valid form data")

        # Create character
        print("Valid form data for creating a character")
        form_data = {
            'first_name': 'John',
            'middle_name': 'Jacob',
            'last_name': 'Jingleheimer Schmidt',
            'gender': 'Man',
            'personality_traits': ['Kind', 'Musical', 'Forgetful']
        }
        form = CharacterForm(data=form_data, story_id=self.story1.id)
        character2 = form.save()

        # Test character creation
        self.assertEqual(character2.full_name, 'John Jacob Jingleheimer Schmidt')
        self.assertEqual(Character.objects.count(), 1)

        # Update character
        print("Valid form data for updating a character")
        form_data['age'] = 42
        form_data['occupation'] = 'Farmer'
        form = CharacterForm(data=form_data, instance=character2)
        character2 = form.save()

        # Test character update
        self.assertEqual(character2.age, 42)
        self.assertEqual(character2.occupation, 'Farmer')

        # Delete character 2
        print("Deleteing character 2")
        character2.delete()

        # Test character deletion
        self.assertFalse(
            Character.objects.filter(
                last_name='Jingleheimer Schmidt',
                story_id=self.story1.id
            ).exists()
        )
        self.assertEqual(Character.objects.count(), 0)


    ### Teardown

    def tearDown(self):

        print("Model Test Teardown")

        # Delete story object and user object
        self.story1.delete()
        self.author1.delete()
        return super().tearDown()
