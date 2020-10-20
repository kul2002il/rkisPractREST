from rest_framework import serializers
from .models import Post


class SerPost(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('title', 'datetime', 'anons', 'text', 'tags', 'image')
