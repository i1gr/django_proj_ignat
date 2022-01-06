"""djangoignat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from news.views import home, news, article
from service.views import order, service
from users.views import login, sign_in, sign_up

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('news/', news, name='news'),
    path('order/', order, name='order'),
    path('login/', login, name='login'),
    path('login/sign_in/', sign_in, name='sign_in'),
    path('login/sign_up/', sign_up, name='sign_up'),
    path('service/<slug:service_slug>/', service, name='service'),
    path('news/<slug:article_slug>/', article, name='article')
]
