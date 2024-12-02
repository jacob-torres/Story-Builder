from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stories/', views.stories, name='stories'),
    path('stories/new/', views.create_or_update_story, name='new_story'),
    path('stories/<int:story_id>/', views.story_detail, name='story_detail'),
    path('stories/<int:story_id>/update/', views.create_or_update_story, name='update_story'),
    path('stories/<int:story_id>/delete/', views.delete_story, name='delete_story'),
    # path('stories/<int:story_id>/scenes/', views.scenes, name='scenes'),
    path('stories/<int:story_id>/new-scene/', views.new_scene, name='new_scene'),
    path('stories/<int:story_id>/scene-<int:scene_id>/', views.scene_detail, name='scene_detail'),
    path('stories/<int:story_id>/scene-<int:scene_id>/update/', views.update_scene, name='update_scene'),
    path('stories/<int:story_id>/scene-<int:scene_id>/delete/', views.delete_scene, name='delete_scene'),
    path('stories/<int:story_id>/new-character/', views.new_character, name='new_character'),
    path('stories/<int:story_id>/character-<int:character_id>/', views.character_detail, name='character_detail'),
    path('stories/<int:story_id>/character-<int:character_id>/update/', views.update_character, name='update_character'),
    path('stories/<int:story_id>/character-<int:character_id>/delete/', views.delete_character, name='delete_character'),
]