from django.urls import path

from news.views import NewsProfileView
from .views import index
from users.views import ProfileView


urlpatterns = [
    path('test/', index),
    path('prof/', ProfileView.as_view()),
    path('mynews/', NewsProfileView.as_view()),

    path('accounts/profile/', index, name='profile'),
]
