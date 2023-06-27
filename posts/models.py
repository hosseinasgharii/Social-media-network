from django.db import models
from accounts.models import MyUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class PostModel(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE
        )
    caption = models.TextField(
        blank=True,
        null=True,
        max_length=500,
        verbose_name="Caption")
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
        )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated At"
        )
    slug = models.SlugField(
        verbose_name="Slug"
        )
    location = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        verbose_name="Location"
        )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
        )

    def report_post(self, user, reason):
        Report.objects.create(user=user, post=self, reason=reason)

    def __str__(self) -> str:
        return self.slug


class Image(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=50
        )
    alt = models.CharField(
        _("Text"),
        max_length=100
        )
    image = models.ImageField(
        _("Image"),
        upload_to="uploads/image",
        )
    post = models.ForeignKey(
        PostModel,
        related_name="images",
        on_delete=models.CASCADE
        )

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE
        )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE
        )

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    def __str__(self):
        return f"{self.user.username} liked {self.post.slug}"


class Comment(models.Model):
    comment_text = models.CharField(
        max_length=128,
        verbose_name="Comment"
        )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE
        )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE
        )
    reply_to = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="reply"
        )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Create At"
        )
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Parent Comment"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child")

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"comment on {self.post.slug}"


class Report(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="reporter"
        )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="reported_post"
        )
    reason = models.TextField(
        max_length=500
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
        related_name='sent_posts'
        )
    recipient = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='received_posts'
        )
    post = models.ForeignKey(
        PostModel,
        on_delete=models.CASCADE
        )
    sent_at = models.DateTimeField(
        default=timezone.now
        )

    def __str__(self):
        return f"{self.sender} sent post {self.post.slug} to {self.recipient}"
