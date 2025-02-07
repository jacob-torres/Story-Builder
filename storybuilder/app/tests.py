from django.test import TestCase
from .models import Story, Scene, Character, Plot, PlotPoint

# Create your tests here.
class StoryModelTest(TestCase):
    """Test case for the Story model."""

    def setUp(self):

        # Create new story object
        self.story1 = Story.objects.create(
            title='Story 1',
            description='Description for Story 1.',
            author_id=1
        )

        return super().setUp()

    def test_story_creation(self):
        """Test story creation."""

        print("*****************************")
        print("Testing Story Creation ...")

        # Run tests
        self.assertEqual(self.story1.title, 'Story 1')
        self.assertEqual(self.story1.description, 'Description for Story 1.')
        self.assertEqual(self.story1.author_id, 1)
        self.assertEqual(Story.objects.count(), 1)

    def tearDown(self):

        # Delete story object
        self.story1.delete()
        return super().tearDown()