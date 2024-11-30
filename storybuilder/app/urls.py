from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stories/', views.stories, name='stories'),
    path('stories/new/', views.new_story, name='new_story'),
    path('stories/<int:story_id>/', views.story_detail, name='story_detail'),
    path('stories/<int:story_id>/update/', views.update_story, name='update_story'),
    path('stories/<int:story_id>/delete/', views.delete_story, name='delete_story'),
    path('stories/<int:story_id>/scenes/', views.scenes, name='scenes'),
    path('stories/<int:story_id>/scenes/new/', views.new_scene, name='new_scene'),
    path('stories/<int:story_id>/scenes/<int:scene_id>/', views.scene_detail, name='scene_detail'),
    path('stories/<int:story_id>/scenes/<int:scene_id>/update/', views.update_scene, name='update_scene'),
    path('stories/<int:story_id>/scenes/<int:scene_id>/delete/', views.delete_scene, name='delete_scene')
]