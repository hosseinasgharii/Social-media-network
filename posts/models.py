from django.db import models
from accounts.models import MyUser
# Create your models here.
class PostModel(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    caption = models.TextField(blank=True,null=True, max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    location = models.CharField(blank=True,null=True,max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.slug