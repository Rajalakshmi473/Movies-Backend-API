from django.urls import path
from App.views import MovieListCreateAPIView, MovieRetrieveUpdateAPIView, delete_actor

urlpatterns = [
    path('movies/', MovieListCreateAPIView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', MovieRetrieveUpdateAPIView.as_view(), name='movie-retrieve-update'),
    path('actors/<int:pk>/delete/', delete_actor, name='delete-actor'),
]
