from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Movie, Actor
from .Serializers import MovieSerializer, ActorSerializer

class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

@api_view(['POST'])
def delete_actor(request, pk):
    try:
        actor = Actor.objects.get(pk=pk)
        if not actor.movies.exists():
            actor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Actor is associated with movies and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
    except Actor.DoesNotExist:
        return Response({"detail": "Actor not found."}, status=status.HTTP_404_NOT_FOUND)
