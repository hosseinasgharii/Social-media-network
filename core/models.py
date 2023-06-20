from django.db import models
from django.shortcuts import get_object_or_404
from accounts.models import MyUser
from posts.models import PostModel

def report_post(user_id, post_id, reason):
    user = get_object_or_404(MyUser, id=user_id)
    post = get_object_or_404(PostModel, id=post_id)
    post.report_post(user, reason)

def report_account(user_id, account_id, reason):
    user = get_object_or_404(MyUser, id=user_id)
    account = get_object_or_404(MyUser, id=account_id)
    account.report_account(user, reason)