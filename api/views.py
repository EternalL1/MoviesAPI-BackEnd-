from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import User
from .models import Movie, Review, Bookmark
from .serializers import MovieSerializer, ReviewSerializer, BookmarkSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, viewsets, permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Count

def normalize_phone(phone):
    """ Convert phone number to a consistent format (e.g., +639123456789) """
    phone = phone.replace(" ", "").replace("-", "") 
    if phone.startswith("+63"):  
        return phone  
    elif phone.startswith("09"):  
        return "+63" + phone[1:]  
    elif phone.startswith("9") and len(phone) == 10:  
        return "+63" + phone  
    return phone  

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    if request.method == 'POST':
        fullName = request.data.get('fullName', None)
        email = request.data.get('email', None)
        phoneNumber = request.data.get('phoneNumber', None)
        password = request.data.get('password', None)

        if not fullName or not password or (not email and not phoneNumber):
            return JsonResponse({'error': 'Full name, password, and either email or phone number are required'}, status=400)
        
        if phoneNumber:
            phoneNumber = normalize_phone(phoneNumber)  # Normalize before saving
        
        user = User.objects.create_user(
            fullName=fullName,
            email=email,
            phoneNumber=phoneNumber,
            password=password 
        )
        return JsonResponse({'message': 'User registered successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    if request.method == 'POST':
        identifier = request.data.get('identifier', None)
        password = request.data.get('password', None)

        if not identifier or not password:
            return JsonResponse({'error': 'Identifier and password are required'}, status=400)

        user = User.objects.filter(email=identifier).first()

        if not user:
            normalized_phone = normalize_phone(identifier)
            user = User.objects.filter(phoneNumber=normalized_phone).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({
                'message': 'Login successful',
                'token': token.key,
                'role': user.role 
            }, status=200)

        return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405) 


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_movie(request):
    if request.user.role != 'admin': 
        return Response({'error': 'You do not have permission to add movies'}, status=403)

    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


class MovieDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = []


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def coming_soon_movies(request):
    today = timezone.now().date()
    movies = Movie.objects.filter(release_date__gt=today) 
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def released_movies(request):
    today = timezone.now().date()
    movies = Movie.objects.filter(release_date__lte=today)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data) 

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_movies(request):
    query = request.GET.get('q', '') 
    movies = Movie.objects.filter(title__icontains=query)  
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_reviews(request, movie_id):
    reviews = Review.objects.filter(movie_id=movie_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user, movie=movie) 
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def update_delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        review.delete()
        return Response({'message': 'Review deleted successfully'}, status=204)
    

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_genres(request):
    try:
        movies = Movie.objects.all()
        
        genre_counts = {}
        
        for movie in movies:
            genres = [g.strip().title() for g in movie.genre.split(',')]
            
            for genre in genres:
                if genre:  
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        genre_data = [
            {
                'genre': genre,
                'count': count
            }
            for genre, count in genre_counts.items()
        ]
        
        genre_data.sort(key=lambda x: x['genre'])
        
        return Response(genre_data)
    except Exception as e:
        print("Error in get_genres:", str(e))
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def movies_by_genre(request, genre):
    try:
        genre = genre.title()
        
        movies = Movie.objects.all()
        matching_movies = []
        
        for movie in movies:
            movie_genres = [g.strip().title() for g in movie.genre.split(',')]
            
            if genre in movie_genres:
                matching_movies.append(movie)
        
        print(f"Looking for genre: {genre}")
        print(f"Found {len(matching_movies)} movies")
        
        serializer = MovieSerializer(matching_movies, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in movies_by_genre: {str(e)}")
        return Response({'error': str(e)}, status=500)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Movie.objects.all()
        genre = self.request.query_params.get('genre', None)
        
        if genre:
            genres = [g.strip().title() for g in genre.split(',')]
            matching_movies = []
            
            for movie in queryset:
                movie_genres = [g.strip().title() for g in movie.genre.split(',')]
                if any(g in movie_genres for g in genres):
                    matching_movies.append(movie)
            
            return matching_movies
        
        return queryset 
    

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    serializer = BookmarkSerializer(bookmarks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_bookmark(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if Bookmark.objects.filter(user=request.user, movie=movie).exists():
        return Response({'error': 'Movie is already bookmarked'}, status=status.HTTP_400_BAD_REQUEST)
    
    bookmark = Bookmark.objects.create(user=request.user, movie=movie)
    serializer = BookmarkSerializer(bookmark)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_bookmark(request, movie_id):
    bookmark = Bookmark.objects.filter(user=request.user, movie_id=movie_id).first()
    
    if not bookmark:
        return Response({'error': 'Bookmark not found'}, status=status.HTTP_404_NOT_FOUND)
    
    bookmark.delete()
    return Response({'message': 'Bookmark removed'}, status=status.HTTP_204_NO_CONTENT)