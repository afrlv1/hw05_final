from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст', help_text=u'Введите текст...')
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_posts')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name='group_posts',verbose_name='Группа', help_text=u'Выберите группу...')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comments')
    text = models.TextField(verbose_name='Текст', help_text=u'Введите текст комментария')
    created = models.DateTimeField('Дата и время публикации', auto_now_add=True,db_index=True)

    def __str__(self):
        return self.title