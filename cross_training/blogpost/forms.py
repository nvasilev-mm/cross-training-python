from django import forms
from . import models

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ["title", "content"]

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ["content"]