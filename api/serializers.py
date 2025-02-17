from rest_framework import serializers
from .models import Movie, User, Review

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'description', 'release_date', 
                 'poster_image', 'average_rating', 'duration', 'main_cast', 
                 'director', 'video_url'] 

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