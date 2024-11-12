from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def welcome(request):
    """Welcome page."""
    return render(request, 'welcome.html')

def login(request):
    """Login view."""
    return render(request, 'login.html')

def logout(request):
    """Logout view."""
    logout(request)
    return redirect('')  # Redirect to welcome/home page

def signup(request):
    """Signup view."""
    return render(request, 'signup.html')
