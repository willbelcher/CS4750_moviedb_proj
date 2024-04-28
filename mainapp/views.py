from django.shortcuts import render


def home(request):

    return render(request, 'mainapp/home.html')


def movie_search(request):

    return render(request)


def login_view(request):

    return render(request)


def logout_view(request):

    return render(request)

