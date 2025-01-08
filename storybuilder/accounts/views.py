from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import CustomUser, UserProfile


def register(request):
    """View function for registering a new user account."""

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('login') 
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """View function for logging in an existing user."""

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """View function for logging out an existing user."""

    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home')


def profile(request):
    """View function for rendering and updating a user profile."""

    if request.user.is_authenticated:
        user = request.user
        try:
            user_profile = user.profile
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=user) 
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                user_profile = form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
        else:
            form = UserProfileForm(instance=user_profile)
        return render(request, 'accounts/update_profile.html', {'form': form})
    else:
        return redirect('login')
