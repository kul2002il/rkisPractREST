from django.urls import path
from .views import ViewLogin, viewPost, viewComments, viewPostDetail


urlpatterns = [
	path('auth/', ViewLogin.as_view()),
	path('posts/', viewPost),
	path('posts/<int:pk>/', viewPostDetail),
	path('posts/<int:pk>/comments/', viewComments),
]

