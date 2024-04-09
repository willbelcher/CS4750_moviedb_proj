from django.shortcuts import render


def home(request):

    return render(request, 'home.html')


def login_view(request):

    return render(request)


def logout_view(request):

    return render(request)

