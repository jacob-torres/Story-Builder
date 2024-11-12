from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm

# Create your views here.
def welcome(request):
    """Welcome page."""
    return render(request, 'welcome.html')

def login_view(request):
    """Login view."""

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('')
            else:
                form.add_error(None, 'Invalid username or password')

    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'login.html', context=context)

def logout_view(request):
    """Logout view."""
    logout(request)
    return redirect('')  # Redirect to welcome/home page

def signup_view(request):
    """Signup view."""
    return render(request, 'signup.html')
