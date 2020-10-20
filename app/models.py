from django.db import models
from django.contrib.auth.models import AbstractUser

from .utilities import get_timestamp_path


class User(AbstractUser):
	class Meta(AbstractUser.Meta):
		pass


class Tag(models.Model):
	name = models.CharField(max_length=255, verbose_name='Заголовок')


class Post(models.Model):
	title = models.CharField(max_length=255, verbose_name='Заголовок')
	datetime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата публикации')
	anons = models.CharField(max_length=254, verbose_name='Краткая информация о новости.')
	text = models.CharField(max_length=255, verbose_name='Текст')
	tags = models.ManyToManyField(Tag)
	image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name="comments")
	author = models.CharField(max_length=255, verbose_name='Автор')
	comment = models.TextField(max_length=255, verbose_name='Текст')
	datetime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата публикации')

