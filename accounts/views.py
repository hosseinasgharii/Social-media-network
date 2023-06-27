from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from accounts.models import MyUser, Relationship
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import PostModel
from django.http import HttpResponse


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

        return redirect('accounts:login')

    return render(request, 'accounts/signup.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Invalid email or password.")
            return render('accounts/login.html')

    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in first.")
        return redirect('accounts:login')

    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('accounts:login')


@login_required
def profile(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user

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
        return render(request, 'accounts/edit_profile.html')


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
def block_user(request, user_id):
    user = request.user
    blocked_user = get_object_or_404(MyUser, id=user_id)

    if user.is_authenticated and user != blocked_user:
        if not user.is_blocked(blocked_user):
            user.block_user(blocked_user)
            return HttpResponse("User blocked successfully.")
        else:
            return HttpResponse("User is already blocked.")

    return HttpResponse("Invalid request.")
