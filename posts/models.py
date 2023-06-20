from django.db import models
from accounts.models import MyUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class PostModel(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    caption = models.TextField(blank=True,null=True, max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    location = models.CharField(blank=True,null=True,max_length=50)
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(MyUser, related_name="liked_posts", blank=True)

    def like_post(self, user):
        self.likes.add(user)

    def unlike_post(self, user):
        self.likes.remove(user)

    def has_liked_post(self, user):
        return self.likes.filter(pk=user.pk).exists()
    
    def report_post(self, user, reason):
        Report.objects.create(user=user, post=self, reason=reason)

    def __str__(self) -> str:
        return self.slug
    
class Image(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    alt = models.CharField(_("Text"), max_length=100)
    image = models.ImageField(_("Image"), upload_to="uploads/image",)
    post = models.ForeignKey(PostModel, related_name="images", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    comment_text = models.CharField(max_length=128)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel,on_delete=models.CASCADE)
    reply_to = models.ForeignKey("self", blank=True, null=True,on_delete=models.CASCADE) 
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"comment on {self.post.slug}"


class Report(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, blank=True, null=True)
    account = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='reported_accounts', blank=True, null=True)
    reason = models.TextField(max_length=500)

    def __str__(self):
        if self.post:
            return f"Report on post: {self.post.slug}"
        elif self.account:
            return f"Report on account: {self.account.username}"
        else:
            return "Invalid report"
    