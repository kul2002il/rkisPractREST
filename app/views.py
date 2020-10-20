from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import User, Tag, Post, Comment
from .serializers import SerPost, SerComment


@api_view(['GET'])
def viewPost(request):
	if request.method == 'GET':
		bbs = Post.objects.all()[:10]
		serializer = SerPost(bbs, many=True)
		return Response(serializer.data)


@api_view(['GET'])
def viewPostDetail(request, pk):
	post = Post.objects.filter(id=pk)[0]
	serPost = SerPost(post, many=False)
	comments = Comment.objects.filter(post=pk)
	serCom = SerComment(comments, many=True)
	data = {
		'serPost': serPost.data,
		'serCom': serCom.data
	}
	return Response(data)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def viewComments(request, pk):
	if request.method == 'POST':
		serializer = SerComment(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return  Response(serializer.data, status=HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
	else:
		comments = Comment.objects.filter(post=pk)
		serializer = SerComment(comments, many=True)
		return Response(serializer.data)
