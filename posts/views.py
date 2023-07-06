from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import PostModel, Comment, Report, SendPost, Image
from accounts.models import MyUser
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import CreatePostForm, CommentForm, ReplyForm, ReportForm, PostForm
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

class CreatePostView(View):
    def get(self, request):
        form = CreatePostForm()
        return render(request, 'posts/create_post.html', {'form': form})

    def post(self, request):
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.user.id
            caption = form.cleaned_data['caption']
            slug = slugify(form.cleaned_data['caption'][:20])
            location = form.cleaned_data['location']
            image = form.cleaned_data['image']
            user = MyUser.objects.get(id=user_id)
            post = PostModel(
                user=user,
                caption=caption,
                slug=slug,
                location=location
            )
            post.save()

            Image.objects.create(
                name=image.name,
                alt="",
                image=image,
                post=post
            )

            return redirect('accounts:profile', request.user.id)
        return render(request, 'posts/create_post.html', {'form': form})


class PostDetailView(View):
    def get(self, request, slug):
        post = get_object_or_404(PostModel, slug=slug)
        comments = Comment.objects.filter(post=post, parent=None)
        return render(
            request,
            'posts/post_detail.html',
            {'post': post, 'comments': comments}
            )

    def post(self, request, slug):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment_text']
            post = get_object_or_404(PostModel, slug=slug)
            Comment.objects.create(
                comment_text=comment_text,
                user=request.user,
                post=post)
            return redirect("posts:post_detail", post.slug)
        return redirect("posts:post_detail", slug)


@method_decorator(require_POST, name='dispatch')
class LikePostView(View):
    def post(self, request):
        post_id = request.POST.get('post_id')
        post = PostModel.objects.get(id=post_id)
        post.like_post(request.user)
        return HttpResponse({'message': 'Post liked successfully'})


@method_decorator(require_POST, name='dispatch')
class UnlikePostView(View):
    def post(self, request):
        post_id = request.POST.get('post_id')
        post = PostModel.objects.get(id=post_id)
        post.unlike_post(request.user)
        return HttpResponse({'message': 'Post unliked successfully'})


class CommentPostView(View):
    @require_POST
    def post(self, request):
        post_id = request.POST.get('post_id')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment_text']
            post = get_object_or_404(PostModel, id=post_id)
            Comment.objects.create(
                comment_text=comment_text,
                user=request.user,
                post=post)
            return HttpResponse({'message': 'Comment added successfully'})
        return HttpResponse({'message': 'Invalid form data'})


class ReplyCommentView(View):
    @require_POST
    def post(self, request):
        comment_id = request.POST.get('comment_id')
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply_text = form.cleaned_data['reply_text']
            comment = get_object_or_404(Comment, id=comment_id)
            Comment.objects.create(
                comment_text=reply_text,
                user=request.user,
                post=comment.post,
                reply_to=comment
            )
            return HttpResponse({'message': 'Reply added successfully'})
        return HttpResponse({'message': 'Invalid form data'})


class ReportPostView(View):
    @require_POST
    def post(self, request):
        post_id = request.POST.get('post_id')
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            post = get_object_or_404(PostModel, id=post_id)
            Report.objects.create(user=request.user, post=post, reason=reason)
            return HttpResponse({'message': 'Post reported successfully'})
        return HttpResponse({'message': 'Invalid form data'})


class ReportAccountView(View):
    @require_POST
    def post(self, request):
        account_id = request.POST.get('account_id')
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            account = get_object_or_404(MyUser, id=account_id)
            Report.objects.create(
                user=request.user,
                account=account,
                reason=reason
                )
            return HttpResponse({'message': 'Account reported successfully'})
        return HttpResponse({'message': 'Invalid form data'})


class SendPostView(View):
    @login_required
    def get(self, request, post_id, recipient_id):
        post = get_object_or_404(PostModel, id=post_id)
        recipient = get_object_or_404(MyUser, id=recipient_id)
        sent_post = SendPost(
            sender=request.user,
            recipient=recipient,
            post=post)
        sent_post.save()
        return HttpResponse("Post sent successfully!")


class PostEditView(View):
    def get(self, request, post_id):
        post = get_object_or_404(PostModel, id=post_id, user=request.user)
        form = PostForm(instance=post)
        return render(
            request,
            'posts/edit_post.html',
            {'form': form, 'post': post}
            )

    def post(self, request, post_id):
        post = get_object_or_404(PostModel, id=post_id, user=request.user)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post.slug)
        return render(
            request,
            'posts/edit_post.html',
            {'form': form, 'post': post}
            )


class PostDeleteView(View):
    def get(self, request, post_id):
        post = get_object_or_404(PostModel, id=post_id, user=request.user)
        return render(request, 'delete_post.html', {'post': post})

    def post(self, request, post_id):
        post = get_object_or_404(PostModel, id=post_id, user=request.user)
        post.delete()
        return redirect(reverse_lazy('accounts/profile.html'))


class DeleteCommentView(View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            comment.delete()
        return redirect("posts:post_detail", slug=comment.post.slug)
