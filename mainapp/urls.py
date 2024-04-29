from django.urls import path

from . import views

app_name = "mainapp"
urlpatterns = [
    path('', views.home, name='home'),
    path('movie-search/', views.search_movies, name='movie_search'),
    path('user-search/', views.search_users, name='user_search'),
    path('logout/', views.handle_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('add-watchlist/<int:movie_id>/<path:next>', views.add_watchlist, name='add_watchlist'),
    path('add-watched/<int:movie_id>/<path:next>', views.add_watched, name='add_watched'),
    path('create-account/', views.create_account, name='create_account'),
    path('user/<str:usr>/', views.list_user_reviews, name='view_user'),
    path('movie/<int:movie_id>/', views.list_movie_reviews, name='view_movie'),
    path('new-review/<int:movie_id>/', views.new_review, name='new_review'),
]
