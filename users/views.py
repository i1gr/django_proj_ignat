from django.shortcuts import render

# Create your views here.



def profile(request):
    return render(request, 'users/profile.html', {'title': "Profile", 'nav_active': 'account'})