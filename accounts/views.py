from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from accounts.models import MyUser, Relationship
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import PostModel


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        MyUser.objects.create_user(
            email=email,
            username=username,
            password=password
            )

        return redirect('login')

    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login')

    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Handle profile edit form submission
        user = request.user

        # Update user profile data
        user.firstname = request.POST['firstname']
        user.lastname = request.POST['lastname']
        user.bio = request.POST['bio']
        user.gender = request.POST['gender']
        user.phonenumber = request.POST['phonenumber']
        user.date_of_birth = request.POST['date_of_birth']

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')
    else:
        # Render the edit profile form
        return render(request, 'edit_profile.html')


@login_required
def follow(request, username):
    # Retrieve the user to follow
    user_to_follow = get_object_or_404(MyUser, username=username)

    # Create a relationship (follower follows following)
    Relationship.objects.create(
        follower=request.user,
        following=user_to_follow)

    messages.success(
        request,
        f"You are now following {user_to_follow.username}."
        )
    return redirect('profile')


@login_required
def unfollow(request, username):
    # Retrieve the user to unfollow
    user_to_unfollow = get_object_or_404(MyUser, username=username)

    # Delete the relationship (follower unfollows following)
    Relationship.objects.filter(
        follower=request.user,
        following=user_to_unfollow).delete()

    messages.success(
        request,
        f"You have unfollowed {user_to_unfollow.username}."
        )
    return redirect('profile')


@login_required
def follower_list(request):
    # Retrieve the user's followers
    followers = Relationship.objects.filter(following=request.user)

    return render(request, 'follower_list.html', {'followers': followers})


@login_required
def following_list(request):
    # Retrieve the user's followings
    followings = Relationship.objects.filter(follower=request.user)

    return render(request, 'following_list.html', {'followings': followings})


@login_required
def posts(request):
    user = request.user
    posts = PostModel.objects.filter(user=user)

    return render(request, 'profile.html', {'posts': posts})


@login_required
def block_member(request, username):
    user_to_block = get_object_or_404(MyUser, username=username)

    Relationship.objects.filter(
        follower=request.user,
        following=user_to_block).delete()

    messages.success(
        request,
        f"You have blocked {user_to_block.username}."
        )
    return redirect('profile')
