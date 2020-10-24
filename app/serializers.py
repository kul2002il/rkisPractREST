from rest_framework import serializers
from .models import User, Tag, Post, Comment


class SerUser(serializers.ModelSerializer):
	login = serializers.CharField(source='username')
	class Meta:
		model = User
		fields = ('login', 'password')
		# extra_kwargs = {'password': {'write_only': True}}


class SerTagId(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ('id','name',)


class SerTag(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ('name',)


class SerPost(serializers.ModelSerializer):
	tags = SerTag(many=True, read_only=True)

	class Meta:
		model = Post
		fields = ('id', 'title', 'datetime', 'anons', 'text', 'tags', 'image')


class SerComment(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('id', 'post', 'author', 'comment', 'datetime')


