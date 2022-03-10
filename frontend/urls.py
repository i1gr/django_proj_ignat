from django.urls import path

from news.views import NewsInProfileView
from .views import profile, service, admin_profile
from users.views import ProfileView


urlpatterns = [
    # path('test/', index),
    path('api/prof/', ProfileView.as_view()),
    path('api/mynews/', NewsInProfileView.as_view()),
    path('t/', profile),

    path('accounts/profile/', profile, name='profile'),
    path('accounts/admin-profile/', admin_profile, name='admin_profile'),
    path('accounts/service/<slug:slug>/', service, name='service'),
]
