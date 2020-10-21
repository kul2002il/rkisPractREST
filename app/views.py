from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
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

			return Response({"token": f"{token}"})
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
		serializer = SerPost(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return  Response(serializer.data, status=HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
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
