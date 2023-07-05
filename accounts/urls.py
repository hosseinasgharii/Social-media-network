from django.urls import path
from accounts.views import (
    UserSignupView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserEditProfileView,
    FollowView,
    UnfollowView,
    FollowerListView,
    FollowingListView,
    PostsView,
    BlockUserView,
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='profile'),
    path('edit-profile/', UserEditProfileView.as_view(), name='edit_profile'),
    path('follow/<str:username>/', FollowView.as_view(), name='follow'),
    path('unfollow/<str:username>/', UnfollowView.as_view(), name='unfollow'),
    path('followers/<int:user_id>/', FollowerListView.as_view(), name='follower_list'),
    path('following/<int:user_id>/', FollowingListView.as_view(), name='following_list'),
    path('posts/', PostsView.as_view(), name='posts'),
    path('block-user/<int:user_id>/', BlockUserView.as_view(), name='block_user'),
]
