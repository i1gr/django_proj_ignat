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
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView

from news.views import home, add_news, NewsPage, article
from service.views import order, service
from users.views import profile

from users.forms import UserLoginForm, UserPasswordResetForm, UserSetPasswordForm, MyCustomUserForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('news/', NewsPage.as_view(), name='news'),
    path('news/add_news', add_news, name='add_news'),
    path('order/', order, name='order'),
    path('service/<slug:service_slug>/', service, name='service'),
    path('news/<slug:article_slug>/', article, name='article'),
    path('accounts/profile/', profile, name='profile'),
]

# registration django-registration
urlpatterns += [
    path('accounts/register/',
         RegistrationView.as_view(
             form_class=MyCustomUserForm
         ),
         name='django_registration_register',
         ),

    path('accounts/',
         include('django_registration.backends.activation.urls')
         ),
]

# login and reset pass
urlpatterns += [
    path(
        'accounts/login/',
        LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
        ),
        name='login'),

    path(
        'accounts/reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            form_class=UserSetPasswordForm
        ),
        name='password_reset'),

    path(
        'accounts/password_reset/',
        PasswordResetView.as_view(
            form_class=UserPasswordResetForm
        ),
        name='password_reset'),

    path('accounts/', include('django.contrib.auth.urls')),

]

# debug toolbar
urlpatterns += [
    path('__debug__/', include('debug_toolbar.urls')),
]
