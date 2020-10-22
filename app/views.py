from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import User, Tag, Post, Comment
from .serializers import SerPost, SerComment, SerUser


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

			print("hdfsdfs")
			print(token)

			res = Response({"token": f"{token}"}, headers={'X-CSRFToken': f"{token}"})
			res.set_cookie('Authorization', f"{token}")  # csrftoken
			return res
		else:
			return Response({"error": "Wrong Credentials"}, status=HTTP_400_BAD_REQUEST)
"""
{
"login": "admin",
"password": "admin"
}
"token": "6477f36bdecd56c6150c2e2419116044cd97fb3c"
"""



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def viewPost(request):
	if request.method == 'POST':
		# if not request.headers['Authorization']:
		# 	return Response({"error": "auth"}, status=HTTP_400_BAD_REQUEST)
		# if not( Post.objects.filter(key=request.headers.Authorization) ):
		# 	return Response({"error": "auth"}, status=HTTP_400_BAD_REQUEST)
		serializer = SerPost(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return  Response(serializer.data, status=HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
	if request.method == 'GET':
		bbs = Post.objects.all()[:10]
		serializer = SerPost(bbs, many=True)
		return Response(serializer.data, headers={'Authorization': "6477f36bdecd56c6150c2e2419116044cd97fb3c"})


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
# @permission_classes((IsAuthenticatedOrReadOnly,))
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


@api_view(['GET'])
def viewPostFromTag(request, name):
	tags = Tag.objects.filter(name=name)
	if not tags:
		return Response({"error": "not tag"}, status=HTTP_404_NOT_FOUND)
	print(tags[0].id)
	bbs = Post.objects.filter(tags__id=tags[0].id)[:10]
	print(bbs)
	serializer = SerPost(bbs, many=True)
	return Response(serializer.data)