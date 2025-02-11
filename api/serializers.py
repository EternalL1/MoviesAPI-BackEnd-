from rest_framework import serializers
from .models import Movie, User, Review

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__' 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phoneNumber', 'fullName', 'role']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'rating', 'review_text', 'created_at']
        read_only_fields = ['user', 'movie']