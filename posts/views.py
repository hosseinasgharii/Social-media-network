from django.shortcuts import render, get_object_or_404 , redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import PostModel, Comment, Report , SendPost
from accounts.models import MyUser
from django.contrib.auth.decorators import login_required

def create_post(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        caption = request.POST.get('caption')
        slug = request.POST.get('slug')
        location = request.POST.get('location')        
        user = MyUser.objects.get(id=user_id)
        post = PostModel(user=user, caption=caption, slug=slug, location=location)
        post.save()
        
        return redirect('post')
    
    return render(request, 'create_post.html')

def post_detail(request, slug):
    post = get_object_or_404(PostModel, slug=slug)
    comments = Comment.objects.filter(post=post, parent=None)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(PostModel, id=post_id)
    post.like_post(request.user)
    return HttpResponse({'message': 'Post liked successfully'})

@require_POST
def unlike_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(PostModel, id=post_id)
    post.unlike_post(request.user)
    return HttpResponse({'message': 'Post unliked successfully'})

@require_POST
def comment_post(request):
    post_id = request.POST.get('post_id')
    comment_text = request.POST.get('comment_text')
    post = get_object_or_404(PostModel, id=post_id)
    Comment.objects.create(comment_text=comment_text, user=request.user, post=post)
    return HttpResponse({'message': 'Comment added successfully'})

@require_POST
def reply_comment(request):
    comment_id = request.POST.get('comment_id')
    reply_text = request.POST.get('reply_text')
    comment = get_object_or_404(Comment, id=comment_id)
    Comment.objects.create(comment_text=reply_text, user=request.user, post=comment.post, reply_to=comment)
    return HttpResponse({'message': 'Reply added successfully'})

@require_POST
def report_post(request):
    post_id = request.POST.get('post_id')
    reason = request.POST.get('reason')
    post = get_object_or_404(PostModel, id=post_id)
    Report.objects.create(user=request.user, post=post, reason=reason)
    return HttpResponse({'message': 'Post reported successfully'})

@require_POST
def report_account(request):
    account_id = request.POST.get('account_id')
    reason = request.POST.get('reason')
    account = get_object_or_404(MyUser, id=account_id)
    Report.objects.create(user=request.user, account=account, reason=reason)
    return HttpResponse({'message': 'Account reported successfully'})

@login_required
def send_post(request, post_id, recipient_id):
    post = get_object_or_404(PostModel, id=post_id)
    recipient = get_object_or_404(MyUser, id=recipient_id)
    sent_post = SendPost(sender=request.user, recipient=recipient, post=post)
    sent_post.save()
    return HttpResponse("Post sent successfully!")