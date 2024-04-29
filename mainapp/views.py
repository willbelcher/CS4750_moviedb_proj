from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from mainapp import db_utils

@login_required
def home(request): # user home page (reviews, watched, watchlist)

    return render(request, 'mainapp/home.html')

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('mainapp:home')
        
        return render(request, 'mainapp/login.html', {'errormsg': 'Incorrect email or password'})

    return render(request, 'mainapp/login.html')

def create_account(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST['name']
        password = request.POST["password"]

        hashed_password = make_password(password)

        success = db_utils.add_user(email, name, hashed_password)

        if not success:
            return render(request, 'mainapp/create_account.html', {'errormsg': 'email already exists'})
        
        user = authenticate(request, username=email, password=password)
        login(request, user)

        return redirect('mainapp:home')
    
    return render(request, 'mainapp/create_account.html')

def handle_logout(request):
    logout(request)
    return redirect('mainapp:login')

@login_required
def search_movies(request):
    movies = []

    if request.method == "POST":
        title = request.POST.get("title")
        min_score = request.POST.get("min_score")

        if len(min_score) == 0: min_score = None

        movies = db_utils.get_movies(title, min_score)
        

    scores = list(range(0, 101))[::-1]
    scores = [x/10 for x in scores]

    return render(request, 'mainapp/search_movies.html', context={'scores': scores, 'movies': movies})

def add_watchlist(request):
    pass

def search_users(request):
    pass

def list_movie_reviews(request, movie_id):
    pass

def list_user_reviews(request, usr):
    if db_utils.get_user(usr) is None:
        return redirect('mainapp:home')

    reviews = db_utils.get_reviews_by_user(usr)
    movies = []
    for review in reviews:
        movies.append(db_utils.get_movie(review[0]))

    return render(request, 'mainapp/user.html', {"reviews":reviews, "movies":movies})

def list_user_watchlist(request):
    pass

def add_review(request):
    pass

def delete_review(request):
    pass

def modify_review(request):
    pass