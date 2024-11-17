from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path    ('stories', views.stories, name='stories'),
    path('stories/new/', views.new_story, name='new_story')
]