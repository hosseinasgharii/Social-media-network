from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('followers/', views.follower_list, name='follower_list'),
    path('following/', views.following_list, name='following_list'),
    path('posts/', views.posts, name='posts'),
    path('block/<str:username>/', views.block_member, name='block_member'),
]