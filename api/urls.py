from django.urls import path, include
from .views import add_bookmark, get_bookmarks, register, login_view, remove_bookmark
from .views import movie_list
from .views import add_movie, movies_by_genre, released_movies
from .views import coming_soon_movies
from .views import search_movies, ReviewViewSet, get_reviews, add_review, update_delete_review, get_genres, MovieViewSet
from .views import MovieDetailView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),

    # Movie URLs
    path('movies/', movie_list, name='movie_list'),
    path('movie/add/', add_movie, name='add_movie'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/coming-soon/', coming_soon_movies, name='coming-soon-movies'),
    path('movies/released/', released_movies, name='released-movies'),
    path('movie/search/', search_movies, name='search-movies'),

    # Review URLs
    path('', include(router.urls)), 
    path('movie/<int:movie_id>/reviews/', get_reviews, name='get_reviews'),
    path('movie/<int:movie_id>/reviews/add/', add_review, name='add_review'),
    path('reviews/<int:review_id>/', update_delete_review, name='update_delete_review'),

    # Genre URLs
    path('genres/', get_genres, name='get-genres'),
    path('movies/genre/<str:genre>/', movies_by_genre, name='movies-by-genre'),
    path('movies/filter/', MovieViewSet.as_view({'get': 'list'}), name='filter-movies'),

    # Bookmarks URLs
    path('bookmarks/', get_bookmarks, name='get_bookmarks'),
    path('bookmarks/add/<int:movie_id>/', add_bookmark, name='add_bookmark'),
    path('bookmarks/remove/<int:movie_id>/', remove_bookmark, name='remove_bookmark'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)