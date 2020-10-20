from django.urls import path
from .views import viewPost, viewComments, viewPostDetail


urlpatterns = [
    path('posts/', viewPost),
	path('posts/<int:pk>/', viewPostDetail),
	path('posts/<int:pk>/comments/', viewComments),
]

