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
	anons = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата публикации')
	text = models.CharField(max_length=255, verbose_name='Текст')
	image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name="comments")
	author = models.CharField(max_length=255, verbose_name='Автор')
	comment = models.TextField(max_length=255, verbose_name='Текст')
	datatime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата публикации')

	def __str__(self):
		return self.comment

