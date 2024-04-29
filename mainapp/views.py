from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from mainapp import db_utils

@login_required
def home(request): # user home page (reviews, watched, watchlist)
    user = request.user

    reviews = db_utils.get_reviews_by_user(user)
    movies = []
    for review in reviews:
        movies.append(db_utils.get_movie(review[0]))

    watchlist = db_utils.get_watchlist(user)

    watched = db_utils.get_watched(user)

    return render(request, 'mainapp/home.html', {"email": user, "reviews":reviews, "movies":movies, "watchlist": watchlist, "watched": watched})

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
        email = request.POST.get("email")
        name = request.POST.get('name')
        number = request.POST.get("phone number")
        password = request.POST.get("password")

        hashed_password = make_password(password)

        success = db_utils.add_user(email, name, number, hashed_password)

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

        movies = db_utils.get_movies_full(title, min_score, get_watched=request.user.email, get_watchlist=request.user.email)
        

    scores = list(range(0, 101))[::-1]
    scores = [x/10 for x in scores]

    return render(request, 'mainapp/search_movies.html', context={'scores': scores, 'movies': movies})

@login_required
def add_watchlist(request, movie_id, next):
    db_utils.add_movie_to_watchlist(request.user.email, movie_id)
    return redirect(next)

@login_required
def add_watched(request, movie_id, next):
    db_utils.add_movie_to_watched(request.user.email, movie_id)
    return redirect(next)

@login_required
def search_users(request):
    users = []

    if request.method == "POST":
        name = request.POST.get("name")
        users = db_utils.get_users(name)
        
    return render(request, 'mainapp/search_users.html', context={'users': users})

@login_required
def list_movie_reviews(request, movie_id):
    if db_utils.get_movie(movie_id) is None:
        return redirect('mainapp:home')
    
    movie = db_utils.get_movie(movie_id)
    reviews = db_utils.get_reviews_by_movie(movie_id)

    return render(request, 'mainapp/movie.html', {"reviews":reviews, "movie":movie})

@login_required
def list_user_reviews(request, usr):
    if db_utils.get_user(usr) is None:
        return redirect('mainapp:home')

    reviews = db_utils.get_reviews_by_user(usr)
    movies = []
    for review in reviews:
        movies.append(db_utils.get_movie(review[0]))

    return render(request, 'mainapp/user.html', {"reviews":reviews, "movies":movies})

@login_required
def list_user_watchlist(request):
    pass

@login_required
def new_review(request, movie_id):
    if db_utils.get_movie(movie_id) is None:
        return redirect('mainapp:home')
    
    movie = db_utils.get_movie(movie_id)

    if request.method == "POST":
        db_utils.add_review(movie_id, request.user, request.POST.get("score"), 
                            request.POST.get("reviewTitle"), request.POST.get("written-review"))
        return redirect('mainapp:home')

    return render(request, 'mainapp/new_review.html', {"movie": movie})

@login_required
def delete_review(request):
    pass

def modify_review(request):
    pass