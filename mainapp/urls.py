from django.urls import path

from . import views

app_name = "mainapp"
urlpatterns = [
    path('', views.home, name='myreviews'),
    path('moviesearch/', views.movie_search, name='moviesearch'),
    path('logout/', views.handle_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('create-account', views.create_account, name='create_account'), # adds to db
]
