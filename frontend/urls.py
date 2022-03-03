from django.urls import path

from news.views import NewsInProfileView
from .views import profile
from users.views import ProfileView


urlpatterns = [
    # path('test/', index),
    path('api/prof/', ProfileView.as_view()),
    path('api/mynews/', NewsInProfileView.as_view()),
    path('t/', profile),

    path('accounts/profile/', profile, name='profile'),
]
