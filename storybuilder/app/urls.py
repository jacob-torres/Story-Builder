from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='Welcome'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup')
]