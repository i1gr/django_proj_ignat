from django.shortcuts import render

# Create your views here.


def login(request):
    return render(request, 'users/login.html', {'title': "Login", 'nav_active': 'account'})


def sign_up(request):
    return render(request, 'users/sign_up.html', {'title': "Sign up", 'nav_active': 'account'})


def sign_in(request):
    return render(request, 'users/sign_in.html', {'title': "Sign in", 'nav_active': 'account'})