from django.urls import path, include
from .views import register, login_view
from .views import movie_list
from .views import add_movie
from .views import coming_soon_movies
from .views import search_movies, ReviewViewSet, get_reviews, add_review, update_delete_review
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
    path('movie/search/', search_movies, name='search-movies'),

    # Review URLs
    path('', include(router.urls)), 
    path('movie/<int:movie_id>/reviews/', get_reviews, name='get_reviews'),
    path('movie/<int:movie_id>/reviews/add/', add_review, name='add_review'),
    path('reviews/<int:review_id>/', update_delete_review, name='update_delete_review'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)