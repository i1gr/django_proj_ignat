from django.urls import path

from service.views import ServicesWithoutOrders

urlpatterns = [
    path('ser/<slug:slug>', ServicesWithoutOrders.as_view()),
]