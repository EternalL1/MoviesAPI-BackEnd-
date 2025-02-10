from django.urls import path
from .views import register, login_view
from .views import movie_list
from .views import add_movie
from .views import coming_soon_movies
from .views import MovieDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('movies/', movie_list, name='movie_list'),
    path('movie/add/', add_movie, name='add_movie'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/coming-soon/', coming_soon_movies, name='coming-soon-movies'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)