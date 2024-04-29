from django.urls import path

from . import views

app_name = "mainapp"
urlpatterns = [
    path('', views.home, name='home'),
    path('movie-search/', views.search_movies, name='movie_search'),
    path('user-search/', views.search_users, name='user_search'),
    path('logout/', views.handle_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('create-account/', views.create_account, name='create_account'), # create account form
    path('add-account', views.create_account, name='add_account'), # adds to db
    path('authenticate/', views.user_login, name='authenticate'),
    path('user/<str:usr>/', views.list_user_reviews, name='view_user'),
    path('movie/<int:movie_id>/', views.list_movie_reviews, name='view_movie'),
    path('add-watchlist/', views.add_watchlist, name='add_watchlist'),
]
