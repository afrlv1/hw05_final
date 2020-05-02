from django.forms import ModelForm
from django import forms
from .models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        # эта форма будет хранить данные в модели
        model = Post
        # на странице формы будут отображаться поля 'group' и 'text'
        fields = ['group', 'text', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {'text': forms.Textarea, }
