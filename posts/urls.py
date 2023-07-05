from django.urls import path
from posts.views import (
    CreatePostView,
    PostDetailView,
    LikePostView,
    UnlikePostView,
    CommentPostView,
    ReplyCommentView,
    ReportPostView,
    ReportAccountView,
    PostEditView
)

app_name = 'posts'

urlpatterns = [
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('like-post/', LikePostView.as_view(), name='like_post'),
    path('unlike-post/', UnlikePostView.as_view(), name='unlike_post'),
    path('comment-post/', CommentPostView.as_view(), name='comment_post'),
    path('reply-comment/', ReplyCommentView .as_view(), name='reply_comment'),
    path('report-post/', ReportPostView.as_view(), name='report_post'),
    path('report-account/', ReportAccountView.as_view(), name='report_account'),
    path('edit-post/<post_id>', PostEditView.as_view(), name='edit_post'),

]
