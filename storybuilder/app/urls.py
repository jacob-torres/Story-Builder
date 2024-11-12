from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='Welcome'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup')
]