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
    path('stories/<slug:story_slug>/new-scene/', views.create_or_update_scene, name='new_scene'),
    path('stories/<slug:story_slug>/scene<int:scene_order>/', views.scene_detail, name='scene_detail'),
    path('stories/<slug:story_slug>/scene<int:scene_order>/update/', views.create_or_update_scene, name='update_scene'),
    path('stories/<slug:story_slug>/scene<int:scene_order>/delete/', views.delete_scene, name='delete_scene'),
    path('stories/<slug:story_slug>/new-character/', views.create_or_update_character, name='new_character'),
    path('stories/<slug:story_slug>/character-<slug:character_slug>/', views.character_detail, name='character_detail'),
    path('stories/<slug:story_slug>/character-<slug:character_slug>/update/', views.create_or_update_character, name='update_character'),
    path('stories/<slug:story_slug>/character-<slug:character_slug>/delete/', views.delete_character, name='delete_character'),
    path('stories/<slug:story_slug>/scene<int:scene_order>/up/', views.move_up, name='move_up'),
    path('stories/<slug:story_slug>/scene<int:scene_order>/down/', views.move_down, name='move_down'),
    path('stories/<slug:story_slug>/plot/', views.plot_detail, name='plot_detail'),
    path('stories/<slug:story_slug>/plot/update/', views.update_plot, name='update_plot'),
    path('stories/<slug:story_slug>/plot/new-plot-point/', views.create_or_update_plot_point, name='new_plot_point'),
    path('stories/<slug:story_slug>/plot/point<int:plot_point_order>/', views.plot_point_detail, name='plot_point_detail'),
    path('stories/<slug:story_slug>/plot/point<int:plot_point_order>/update/', views.create_or_update_plot_point, name='update_plot_point'),
    path('stories/<slug:story_slug>/plot/point<int:plot_point_order>/delete/', views.delete_plot_point, name='delete_plot_point'),
    path('stories/<slug:story_slug>/plot/point<int:plot_point_order>/up/', views.move_up, name='move_up'),
    path('stories/<slug:story_slug>/plot/point<int:plot_point_order>/down/', views.move_down, name='move_down')
]