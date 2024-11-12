from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def welcome(request):
    """Welcome page."""
    return render(request, 'welcome.html')

def login(request):
    """Login view."""
    return render(request, 'login.html')

def logout(request):
    """Logout view."""
    return render(request, 'logout.html')

def signup(request):
    """Signup view."""
    return render(request, 'signup.html')
