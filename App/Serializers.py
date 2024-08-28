from rest_framework import serializers
from .models import Movie, Genre, Actor, Technician, Director

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name']

class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = ['id', 'name']

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)
    technicians = TechnicianSerializer(many=True)
    director = DirectorSerializer()

    class Meta:
        model = Movie
        fields = [
            'id', 'name', 'release_year', 'user_rating',
            'genres', 'actors', 'technicians', 'director'
        ]

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        actors_data = validated_data.pop('actors')
        technicians_data = validated_data.pop('technicians')
        director_data = validated_data.pop('director')
        
        director = Director.objects.create(**director_data)
        movie = Movie.objects.create(director=director, **validated_data)
        
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(**genre_data)
            movie.genres.add(genre)
        
        for actor_data in actors_data:
            actor, created = Actor.objects.get_or_create(**actor_data)
            movie.actors.add(actor)
        
        for technician_data in technicians_data:
            technician, created = Technician.objects.get_or_create(**technician_data)
            movie.technicians.add(technician)
        
        return movie

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres', None)
        actors_data = validated_data.pop('actors', None)
        technicians_data = validated_data.pop('technicians', None)
        director_data = validated_data.pop('director', None)

        if director_data:
            director, created = Director.objects.get_or_create(**director_data)
            instance.director = director
        
        if genres_data:
            instance.genres.clear()
            for genre_data in genres_data:
                genre, created = Genre.objects.get_or_create(**genre_data)
                instance.genres.add(genre)

        if actors_data:
            instance.actors.clear()
            for actor_data in actors_data:
                actor, created = Actor.objects.get_or_create(**actor_data)
                instance.actors.add(actor)

        if technicians_data:
            instance.technicians.clear()
            for technician_data in technicians_data:
                technician, created = Technician.objects.get_or_create(**technician_data)
                instance.technicians.add(technician)

        instance.name = validated_data.get('name', instance.name)
        instance.release_year = validated_data.get('release_year', instance.release_year)
        instance.user_rating = validated_data.get('user_rating', instance.user_rating)
        instance.save()
        return instance
