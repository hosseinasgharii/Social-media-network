from django.contrib import admin
from .models import PostModel , Comment,Image
# Register your models here.

class ImageInline(admin.TabularInline):
    model = Image

class CommentInline(admin.TabularInline):
    model = Comment

class PostModelAdmin(admin.ModelAdmin):
    inlines = [ImageInline, CommentInline]
    list_display = ('slug', 'user', 'create_time', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('slug', 'user_username')
    readonly_fields = ('create_time', 'update_time')
    prepopulated_fields = {'slug': ('caption',)}

admin.site.register(PostModel, PostModelAdmin)
admin.site.register(Comment)
admin.site.register(Image)    
