from django.urls import path

from . import views

app_name = "mainapp"
urlpatterns = [
    path('', views.home, name='myreviews'),
    path('moviesearch/', views.movie_search, name='moviesearch'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login')
]
