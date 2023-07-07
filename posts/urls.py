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
    PostEditView,
    DeleteCommentView,
    PostDeleteView,
    DislikePostView,
    UndislikePostView
)

app_name = 'posts'

urlpatterns = [
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('like/', LikePostView.as_view(), name='like_post'),
    path('unlike/', UnlikePostView.as_view(), name='remove_like'),
    path('dislike/', DislikePostView.as_view(), name='dislike_post'),
    path('undislike/', UndislikePostView.as_view(), name='remove_dislike'),
    path('comment-post/', CommentPostView.as_view(), name='comment_post'),
    path('reply-comment/', ReplyCommentView .as_view(), name='reply_comment'),
    path('report-post/', ReportPostView.as_view(), name='report_post'),
    path('report-account/', ReportAccountView.as_view(), name='report_account'),
    path('edit-post/<post_id>', PostEditView.as_view(), name='edit_post'),
    path('delete-comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('post/<int:post_id>/delete/', PostDeleteView.as_view(), name='delete_post')

]
