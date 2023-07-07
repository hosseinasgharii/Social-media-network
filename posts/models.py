from django.db import models
from accounts.models import MyUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class PostModel(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="show_post",
        help_text="The user who created the post."
    )
    caption = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        verbose_name="Caption",
        help_text="The caption of the post (maximum 500 characters)."
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="when the post was created."
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated At",
        help_text="when the post was last updated."
    )
    slug = models.SlugField(
        verbose_name="Slug",
        help_text="The unique slug for the post URL."
    )
    location = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        verbose_name="Location",
        help_text="The location associated with the post."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="the post is active or not."
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True,
        help_text="Users who have liked the post."
    )
    dislikes = models.ManyToManyField(
        User,
        related_name='dislike_posts',
        blank=True,
        help_text="Users who have disliked the post."
    )

    def report_post(self, user, reason):
        Report.objects.create(user=user, post=self, reason=reason)

    def __str__(self) -> str:
        return self.slug

    def like_post(self, user):
        self.likes.add(user)

    def remove_like(self, user):
        self.likes.remove(user)

    def dislike_post(self, user):
        self.dislikes.add(user)

    def remove_dislike(self, user):
        self.dislikes.remove(user)


class Image(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=50,
        help_text="The name of the image."
    )
    alt = models.CharField(
        _("Text"),
        max_length=100,
        help_text="The alternative text for the image."
    )
    image = models.ImageField(
        _("Image"),
        upload_to="uploads/image",
        help_text="The image file."
    )
    post = models.ForeignKey(
        PostModel,
        related_name="images",
        on_delete=models.CASCADE,
        help_text="The post associated with the image."
    )

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        help_text="The user who liked the post."
    )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        help_text="The post that was liked."
    )

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    @staticmethod
    def is_like(post, user):
        return Like.objects.filter(post=post, user=user).exists()

    def __str__(self):
        return f"{self.user.username} liked {self.post.slug}"


class DisLike(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        help_text="The user who disliked the post."
    )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        help_text="The post that was disliked."
    )

    class Meta:
        verbose_name = _("Dislike")
        verbose_name_plural = _("Dislikes")

    @staticmethod
    def is_dislike(self, user):
        return Like.objects.get(post=self, user=user).exists()

    def __str__(self):
        return f"{self.user.username} disliked {self.post.slug}"


class Comment(models.Model):
    comment_text = models.CharField(
        max_length=128,
        verbose_name="Comment",
        help_text="The comment text (maximum 128 characters)."
    )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        help_text="The user who posted the comment."
    )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        help_text="The post associated with the comment."
    )
    reply_to = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="reply",
        help_text="The comment being replied"
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Create At",
        help_text="when the comment was created."
    )
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Parent Comment"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child",
        help_text="The parent comment"
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"comment on {self.post.slug}"


class Report(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="reporter",
        help_text="The user who reported the post."
    )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="reported_post",
        help_text="The post being reported"
    )
    reason = models.TextField(
        max_length=500,
        help_text="The reason for reporting the post."
    )

    def __str__(self):
        if self.post:
            return f"Report on post: {self.post.slug}"
        else:
            return "Invalid report"


class SendPost(models.Model):
    sender = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='sent_posts',
        help_text="The user who sent the post."
    )
    recipient = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='received_posts',
        help_text="The user who received the post."
    )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        help_text="The post being sent."
    )
    sent_at = models.DateTimeField(
        default=timezone.now,
        help_text="when the post was sent."
    )

    def __str__(self):
        return f"{self.sender} sent post {self.post.slug} to {self.recipient}"
