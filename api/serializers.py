from rest_framework import serializers
from .models import Movie, User, Review, Bookmark

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'release_date', 
                 'poster_image', 'average_rating', 'duration','video_url'] 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phoneNumber', 'fullName', 'role']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'rating', 'review_text', 'created_at']
        read_only_fields = ['user', 'movie']

class BookmarkSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_poster = serializers.CharField(source='movie.poster_image', read_only=True)
    movie_release_date = serializers.CharField(source='movie.release_date', read_only=True)


    class Meta:
        model = Bookmark
        fields = [
            'id', 'user', 'movie', 'movie_id', 'movie_title', 
            'movie_poster', 'movie_release_date', 'created_at'
        ]
        read_only_fields = ['user']
