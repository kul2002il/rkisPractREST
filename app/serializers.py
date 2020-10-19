from rest_framework import serializers
from .models import Post


class View(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('title', 'anons', 'text', 'created_at')
