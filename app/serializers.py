from rest_framework import serializers
from .models import User, Tag, Post, Comment


class SerPost(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('title', 'datetime', 'anons', 'text', 'tags', 'image')


class SerComment(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('post', 'author', 'comment', 'datetime')


