from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from accounts.models import MyUser, Relationship
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from posts.models import PostModel
from django.http import HttpResponse
from accounts.forms import UserLoginForm, UserSignupForm, UserEditProfileForm
from django.views.generic import View, TemplateView


class UserSignupView(View):
    def get(self, request):
        form = UserSignupForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = UserSignupForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            MyUser.objects.create_user(
                email=email,
                username=username,
                password=password
                )
            return redirect('accounts:login')

        return render(request, 'accounts/signup.html', {'form': form})


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect('accounts:profile')

        messages.error(request, "Invalid email or password.")
        return render(request, 'accounts/login.html', {'form': form})


class UserLogoutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in first.")
            return redirect('accounts:login')

        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect('accounts:login')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(MyUser, pk=user_id)
        post = PostModel.objects.filter(user=user)
        context = {'user': user, 'post': post}
        return render(request, 'accounts/profile.html', context=context)


class UserEditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserEditProfileForm(instance=request.user)
        return render(request, 'accounts/edit_profile.html', {'form': form})

    def post(self, request):
        form = UserEditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile', request.user.id)
        else:
            messages.error(request, "Error updating profile.")
            return render(
                request, 'accounts/edit_profile.html', {'form': form}
                )


class FollowView(LoginRequiredMixin, View):
    def get(self, request, username):
        user_to_follow = get_object_or_404(MyUser, username=username)
        Relationship.objects.create(
            follower=request.user,
            following=user_to_follow
        )
        messages.success(
            request, f"You are now following {user_to_follow.username}."
            )
        return redirect('accounts:profile')


class UnfollowView(LoginRequiredMixin, View):
    def get(self, request, username):
        user_to_unfollow = get_object_or_404(MyUser, username=username)
        Relationship.objects.filter(
            follower=request.user,
            following=user_to_unfollow
        ).delete()
        messages.success(
            request, f"You have unfollowed {user_to_unfollow.username}."
            )
        return redirect('accounts:profile')


class FollowerListView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(MyUser, pk=user_id)
        followers = user.get_followers()
        context = {
            'user': user,
            'followers': followers
        }
        return render(request, 'accounts/follower_list.html', context)


class FollowingListView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(MyUser, pk=user_id)
        following = user.get_following()
        context = {
            'user': user,
            'following': following
        }
        return render(request, 'accounts/following_list.html', context)


class PostsView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = PostModel.objects.filter(user=self.request.user)
        return context


class BlockUserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = request.user
        blocked_user = get_object_or_404(MyUser, id=user_id)

        if user.is_authenticated and user != blocked_user:
            if not user.is_blocked(blocked_user):
                user.block_user(blocked_user)
                return HttpResponse("User blocked successfully.")
            else:
                return HttpResponse("User is already blocked.")

        return HttpResponse("Invalid request.")
