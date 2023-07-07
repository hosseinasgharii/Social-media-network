from django import forms
from .models import PostModel, Comment


class CreatePostForm(forms.ModelForm):
    caption = forms.CharField(
        widget=forms.Textarea,
        max_length=500,
        required=True
        )
    location = forms.CharField(
        max_length=50,
        required=False
        )
    image = forms.ImageField(
        required=True
        )

    class Meta:
        model = PostModel
        fields = ['caption', 'location', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.TextInput(attrs={'maxlength': 128}),
        }


class ReplyForm(forms.Form):
    reply_text = forms.CharField(max_length=128)


class ReportForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea,
        max_length=500
        )


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['caption', 'location']
