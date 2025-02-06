from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import CustomUser, UserProfile


def register(request):
    """View function for registering a new user account."""

    print("*************************")
    print("Register New User")

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                print(f"Saved new user with ID {user.id}, creating user profile ...")
                profile = UserProfile.objects.create(user=user)
                print(f"User Profile created with ID {profile.id}")
                messages.success(request, 'Registration successful!')
                print("New user created successfully!")
                print(user)
                return redirect('login') 
            except Exception as error:
                print("There was an error while creating a new user.")
                print(error)

    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }
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

    context = {
        'form': form
    }
    return render(request, 'login.html', context=context)


@login_required
def logout_view(request):
    """View function for logging out an existing user."""

    print("**********************")
    print("Logout Existing User")

    logout(request)
    messages.success(request, 'Logout successful!')
    print("Successfully logged out user")
    print(request.user)
    return redirect('home')


@login_required
def profile(request):
    """View function for rendering user profile."""

    print("*******************************")
    print("Render User Profile")

    # check for user profile, and create one if it doesn't exist
    if request.user.is_authenticated:
        user = request.user
        try:
            profile = user.profile
        except:
            print("No user profile, creating one now ...")
            profile = UserProfile.objects.create(user=user) 
            print(f"Created user profile with ID {profile.id}")

        context = {'user': user, 'profile': profile}
        return render(request, 'profile.html', context=context)
    
    else:
        print("User not logged in")
        return redirect('login')


@login_required
def update_profile(request):
    """View function for updating a user profile."""

    print("*******************************")
    print("Update User Profile")

    # check for user profile, and create one if it doesn't exist
    if request.user.is_authenticated:
        user = request.user
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user) 

        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                profile = form.save()
                messages.success(request, 'Profile updated successfully!')
                print("Successfully updated user profile")
                print(user)
                return redirect('profile')
        else:
            form = UserProfileForm(instance=profile)
        context = {
            'user': user,
            'form': form
        }
        return render(request, 'update_profile.html', context=context)

    else:
        return redirect('login')


@login_required
def delete_user(request):
    """View function for deleting a user account."""

    print("*****************************")
    print("Delete User Account")

    if request.user.is_authenticated:
        try:
            user = request.user
            profile = user.profile

            print(f"Preparing to delete user {user} ...")
            profile.delete()
            user.delete()
            print("Successfully deleted the user.")

        except Exception as error:
            print("***************")
            print("There was an error while deleting the user.")
            print(error)

        return redirect('home')

    else:
        print("User not logged in")
        return redirect('login')
