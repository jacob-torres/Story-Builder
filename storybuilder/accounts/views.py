from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import CustomUser, UserProfile


def register(request):
    """View function for registering a new user account."""

    print("*************************")
    print("Register New User")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful!')
            print("New user created successfully!")
            print(user)
            return redirect('login') 
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context=context)


def login_view(request):
    """View function for logging in an existing user."""

    print("********************************")
    print("Login Existing User")

    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                print("Successfully logged in")
                print(user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                print("Login was unsuccessful")
                print(user)
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'login.html', context=context)


def logout_view(request):
    """View function for logging out an existing user."""

    print("**********************")
    print("Logout Existing User")

    logout(request)
    messages.success(request, 'Logout successful!')
    print("Successfully logged out user")
    print(request.user)
    return redirect('home')


def profile(request):
    """View function for rendering user profile."""

    print("*******************************")
    print("Render User Profile")

    # check for user profile, and create one if it doesn't exist
    if request.user.is_authenticated:
        user = request.user
        try:
            user_profile = user.profile
        except:
            user_profile = UserProfile.objects.create(user=user) 

        context = {'user': user}
        return render(request, 'profile.html', context=context)
    
    else:
        print("User not logged in")
        return redirect('login')


def update_profile(request):
    """View function for updating a user profile."""

    print("*******************************")
    print("Update User Profile")

    # check for user profile, and create one if it doesn't exist
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
                print("Successfully updated user profile")
                print(user)
                return redirect('profile')
        else:
            form = UserProfileForm(instance=user_profile)
        context = {'form': form}
        return render(request, 'update_profile.html', context=context)

    else:
        return redirect('login')
