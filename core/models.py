from django.db import models

# Create your models here.
from accounts.models import MyUser
from posts.models import PostModel

def report_post(user_id, post_id, reason):
    user = MyUser.objects.get(id=user_id)
    post = PostModel.objects.get(id=post_id)
    post.report_post(user, reason)

def report_account(user_id, account_id, reason):
    user = MyUser.objects.get(id=user_id)
    account = MyUser.objects.get(id=account_id)
    account.report_account(user, reason)