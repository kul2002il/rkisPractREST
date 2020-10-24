from django.urls import path
from .views import ViewLogin, viewPost, viewComments, viewPostDetail, viewPostFromTag, viewCommentsDelete, viewTag


urlpatterns = [
	path('auth/', ViewLogin.as_view()),
	path('posts/', viewPost),
	path('posts/<int:pk>/', viewPostDetail),
	path('posts/<int:pk>/comments/', viewComments),
	path('posts/<int:pkPost>/comments/<int:pk>/', viewCommentsDelete),
	path('tags/', viewTag),
	path('posts/tag/<str:name>/', viewPostFromTag),
]

