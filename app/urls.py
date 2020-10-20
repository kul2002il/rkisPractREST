from django.urls import path
from .views import viewPost


urlpatterns = [
    path('posts/', viewPost),
]

