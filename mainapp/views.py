from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from mainapp import db_utils

@login_required
def home(request): # myreviews page

    return render(request, 'mainapp/home.html')


def movie_search(request):

    return render(request)

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('mainapp:myreviews')
        
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

        return redirect('mainapp:myreviews')
    
    return render(request, 'mainapp/create_account.html')

def handle_logout(request):
    logout(request)
    return redirect('mainapp:login')

def search_movies(request):
    pass

def search_users(request):
    pass

def list_movie_reviews(request):
    pass

def list_user_reviews(request, usr):
    if db_utils.get_user(usr) is None:
        redirect('mainapp:myreviews')

    reviews = db_utils.get_reviews_by_user(usr)

    return render(request, 'mainapp/user.html', {"reviews":reviews})

def list_user_watchlist(request):
    pass

def add_review(request):
    pass

def delete_review(request):
    pass

def modify_review(request):
    pass