from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create-post/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('like-post/', views.like_post, name='like_post'),
    path('unlike-post/', views.unlike_post, name='unlike_post'),
    path('comment-post/', views.comment_post, name='comment_post'),
    path('reply-comment/', views.reply_comment, name='reply_comment'),
    path('report-post/', views.report_post, name='report_post'),
    path('report-account/', views.report_account, name='report_account'),
]
