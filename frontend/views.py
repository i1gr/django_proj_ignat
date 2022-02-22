from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title': 'Profile',
        'nav_active': 'account',
    }
    return render(request, 'frontend/index.html', context=context)