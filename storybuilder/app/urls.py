from django.urls import path
from . import views
from . import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('stories/', views.stories, name='stories'),
    path('stories/new/', views.create_or_update_story, name='new_story'),
    path('stories/<slug:story_slug>/', views.story_detail, name='story_detail'),
    path('stories/<slug:story_slug>/update/', views.create_or_update_story, name='update_story'),
    path('stories/<slug:story_slug>/delete/', views.delete_story, name='delete_story'),
    path('stories/<slug:story_slug>/scenes/', views.scenes, name='scenes'),
    path('stories/<slug:story_slug>/scenes/new/', views.create_or_update_scene, name='new_scene'),
    path('stories/<slug:story_slug>/scenes/<int:scene_order>/', views.scene_detail, name='scene_detail'),
    path('stories/<slug:story_slug>/scenes/<int:scene_order>/update/', views.create_or_update_scene, name='update_scene'),
    path('stories/<slug:story_slug>/scenes/<int:scene_order>/delete/', views.delete_scene, name='delete_scene'),
    path('stories/<slug:story_slug>/scenes/<int:scene_order>/up/', views.move_up, name='move_up'),
    path('stories/<slug:story_slug>/scenes/<int:scene_order>/down/', views.move_down, name='move_down'),
    path('stories/<slug:story_slug>/scenes/<int:scene_order>/add-character/', views.add_scene_character, name='add_scene_character'),
    path('stories/<slug:story_slug>/characters/', views.characters, name='characters'),
    path('stories/<slug:story_slug>/characters/new/', views.create_or_update_character, name='new_character'),
    path('stories/<slug:story_slug>/characters/<slug:character_slug>/', views.character_detail, name='character_detail'),
    path('stories/<slug:story_slug>/characters/<slug:character_slug>/update/', views.create_or_update_character, name='update_character'),
    path('stories/<slug:story_slug>/characters/<slug:character_slug>/delete/', views.delete_character, name='delete_character'),
    path('stories/<slug:story_slug>/plot/', views.plot_detail, name='plot_detail'),
    path('stories/<slug:story_slug>/plot/update/', views.update_plot, name='update_plot'),
    path('stories/<slug:story_slug>/plot/new/', views.create_or_update_plotpoint, name='new_plotpoint'),
    path('stories/<slug:story_slug>/plot/point<int:plotpoint_order>/', views.plotpoint_detail, name='plotpoint_detail'),
    path('stories/<slug:story_slug>/plot/point<int:plotpoint_order>/update/', views.create_or_update_plotpoint, name='update_plotpoint'),
    path('stories/<slug:story_slug>/plot/point<int:plotpoint_order>/delete/', views.delete_plotpoint, name='delete_plotpoint'),
    path('stories/<slug:story_slug>/plot/point<int:plotpoint_order>/up/', views.move_up, name='move_up'),
    path('stories/<slug:story_slug>/plot/point<int:plotpoint_order>/down/', views.move_down, name='move_down')
]