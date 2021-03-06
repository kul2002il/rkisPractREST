from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import User, Tag, Post, Comment
from .serializers import SerPost, SerComment, SerUser, SerTagId
from .utilities import checkAuth


class ViewLogin(APIView):
	permission_classes = ()
	serializer_class = SerUser

	def post(self, request,):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)

		data = serializer.data

		username = data["login"]
		password = data["password"]

		user = authenticate(username=username, password=password)
		if user:
			token, created = Token.objects.get_or_create(user=user)

			return Response({'status': 'true', "token": f"{token}"}, status=HTTP_200_OK)
		else:
			return Response({'status': 'false', 'message': 'Invalid authorization data'}, status=HTTP_401_UNAUTHORIZED)
"""
{
"login": "admin",
"password": "admin"
}
"token": "6477f36bdecd56c6150c2e2419116044cd97fb3c"
"""



@api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticatedOrReadOnly,))
def viewPost(request):
	if request.method == 'POST':
		#
		check = checkAuth(request)
		if check:
			return check
		#
		serializer = SerPost(data=request.data)
		if serializer.is_valid():
			# serializer.data.image = request.FILES.image
			serializer.save()
			id = Post.objects.get(title=serializer.data['title']).id
			return Response({'status': 'true', "post_id": f"{id}"}, status=HTTP_201_CREATED)
		else:
			return Response({'status': 'false', "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
	if request.method == 'GET':
		bbs = Post.objects.all()
		serializer = SerPost(bbs, many=True)
		return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
def viewPostDetail(request, pk):
	if request.method == 'GET':
		post = Post.objects.filter(id=pk)
		if not post:
			return Response({'error': 'NotFoundPost'}, status=HTTP_404_NOT_FOUND)
		else:
			post = post[0]
		serPost = SerPost(post, many=False)
		comments = Comment.objects.filter(post=pk)
		serCom = SerComment(comments, many=True)
		data = {
			'serPost': serPost.data,
			'serCom': serCom.data
		}
		return Response(data)
	else:
		#
		check = checkAuth(request)
		if check:
			return check
		#
		if request.method == 'POST':
			post = Post.objects.get(id=pk)
			if not post:
				return Response({'error': 'NotFoundPost'}, status=HTTP_404_NOT_FOUND)
			#
			serializer = SerPost(data=request.data)
			if serializer.is_valid():
				data = serializer.data
				# for key in data:
				# 	post[key] = data[key]
				if 'title' in data:
					post.title = data['title']
				if 'anons' in data:
					post.anons = data['anons']
				if 'text' in data:
					post.text = data['text']
				if 'tags' in data:
					post.tags = data['tags']
				if 'image' in data:
					post.image = data['image']
				post.save()
				return Response({'message': 'Success'}, status=HTTP_201_CREATED)
			else:
				return Response({'error': 'NotFoundPost'}, status=HTTP_400_BAD_REQUEST)
		if request.method == 'DELETE':
			comm = Post.objects.get(id=pk)
			if comm:
				comm.delete()
				return Response({'message': 'Success'}, status=HTTP_201_CREATED)
			else:
				return Response({'error': 'NotFoundPost'}, status=HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticatedOrReadOnly,))
def viewComments(request, pk):
	if request.method == 'POST':
		#
		check = checkAuth(request)
		if check:
			return check
		#
		serializer = SerComment(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
	else:
		comments = Comment.objects.filter(post=pk)
		serializer = SerComment(comments, many=True)
		return Response(serializer.data)


@api_view(['DELETE'])
# @permission_classes((IsAuthenticatedOrReadOnly,))
def viewCommentsDelete(request, pkPost, pk):
	#
	check = checkAuth(request)
	if check:
		return check
	#
	comm = Comment.objects.get(id=pk)
	if comm:
		comm.delete()
		return Response({'message': 'Success'}, status=HTTP_201_CREATED)
	else:
		return Response({'error': 'NotFoundComment'}, status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
def viewPostFromTag(request, name):
	tags = Tag.objects.filter(name=name)
	if not tags:
		return Response({"error": "not tag"}, status=HTTP_404_NOT_FOUND)
	print(tags[0].id)
	bbs = Post.objects.filter(tags__id=tags[0].id)
	print(bbs)
	serializer = SerPost(bbs, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def viewTag(request):
	bbs = Tag.objects.all()
	serializer = SerTagId(bbs, many=True)
	return Response(serializer.data)