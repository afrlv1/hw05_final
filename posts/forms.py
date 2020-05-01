from django.forms import ModelForm
from django import forms
from .models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        required= {'group': False,}
        widgets = {
            'text': forms.Textarea,
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea,
        }