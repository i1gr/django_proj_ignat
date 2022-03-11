from django.urls import path

from service.views import \
    ServicesApiWithoutOrders, make_order_successful, make_order, OrdersApiForCustomers, OrdersApiForExecutors

urlpatterns = [
    path('service/order-successful/', make_order_successful, name='make_order_successful'),
    path('service/<slug:service_slug>/', make_order, name='make_order'),
    path('api/service-without-order/<slug:slug>/', ServicesApiWithoutOrders.as_view()),
    path('api/customer-orders/', OrdersApiForCustomers.as_view()),
    path('api/executor-orders/', OrdersApiForExecutors.as_view()),

]
