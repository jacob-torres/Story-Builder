from django.urls import path
from . import views
from . import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('stories/', views.stories, name='stories'),
    path('stories/new/', views.create_or_update_story, name='new_story'),
    path('stories/<int:story_id>/', views.story_detail, name='story_detail'),
    path('stories/<int:story_id>/update/', views.create_or_update_story, name='update_story'),
    path('stories/<int:story_id>/delete/', views.delete_story, name='delete_story'),
    path('stories/<int:story_id>/new-scene/', views.create_or_update_scene, name='new_scene'),
    path('stories/<int:story_id>/scene-<int:scene_id>/', views.scene_detail, name='scene_detail'),
    path('stories/<int:story_id>/scene-<int:scene_id>/update/', views.create_or_update_scene, name='update_scene'),
    path('stories/<int:story_id>/scene-<int:scene_id>/delete/', views.delete_scene, name='delete_scene'),
    path('stories/<int:story_id>/new-character/', views.create_or_update_character, name='new_character'),
    path('stories/<int:story_id>/character-<int:character_id>/', views.character_detail, name='character_detail'),
    path('stories/<int:story_id>/character-<int:character_id>/update/', views.create_or_update_character, name='update_character'),
    path('stories/<int:story_id>/character-<int:character_id>/delete/', views.delete_character, name='delete_character'),
    path('stories/<int:story_id>/scene-<int:scene_id>/up/', views.move_up, name='move_up'),
    path('stories/<int:story_id>/scene-<int:scene_id>/down/', views.move_down, name='move_down'),
    path('stories/<int:story_id>/plot/point-<int:plot_point_id>/up/', views.move_up, name='move_up'),
    path('stories/<int:story_id>/plot/point-<int:plot_point_id>/down/', views.move_down, name='move_down')
]