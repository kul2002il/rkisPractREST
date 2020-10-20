from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Post
from .serializers import SerPost


@api_view(['GET'])
def viewPost(request):
   if request.method == 'GET':
       bbs = Post.objects.all()[:10]
       serializer = SerPost(bbs, many=True)
       return Response(serializer.data)

