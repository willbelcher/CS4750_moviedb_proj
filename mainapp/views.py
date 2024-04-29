from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from mainapp import db_utils

@login_required
def home(request): # myreviews page

    return render(request, 'mainapp/home.html')


def movie_search(request):

    return render(request)


def handle_login(request):
    email = request.POST.get("email", None)
    password = request.POST.get("password", None)

    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        return redirect('mainapp:myreviews')
     
    return redirect('mainapp:login')

def login_view(request):

    return render(request, 'mainapp/login.html')

# renders form
def create_account_view(request):

    return render(request, 'mainapp/create_account.html')

# handles account insertion into db
def create_account(request):
    email = request.POST["email"]
    name = request.POST['name']
    password = request.POST["password"]

    success = db_utils.add_user(email, name, password)

    if not success:
        return redirect('mainapp:create_account')
    
    user = authenticate(request, username=email, password=password)
    login(request, user)

    return redirect('mainapp:myreviews')

def handle_logout(request):
    logout(request)
    return redirect('mainapp:login')

def search_movies(request):
    pass

def search_users(request):
    pass

def list_movie_reviews(request):
    pass

def list_user_reviews(request):
    pass

def add_review(request):
    pass

def delete_review(request):
    pass

def modify_review(request):
    pass