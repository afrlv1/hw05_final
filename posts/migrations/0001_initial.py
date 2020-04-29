# Generated by Django 2.2 on 2020-04-23 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст...', verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_posts', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(blank=True, help_text='Выберите группу...', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_posts', to='posts.Group', verbose_name='Группа')),
            ],
        ),
    ]
