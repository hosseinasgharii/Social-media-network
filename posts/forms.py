from django import forms


class CreatePostForm(forms.Form):
    user_id = forms.IntegerField()
    caption = forms.CharField(widget=forms.Textarea, max_length=500, required=True)
    slug = forms.SlugField()
    location = forms.CharField(max_length=50, required=False)


class CommentForm(forms.Form):
    comment_text = forms.CharField(max_length=128)


class ReplyForm(forms.Form):
    reply_text = forms.CharField(max_length=128)


class ReportForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, max_length=500)
