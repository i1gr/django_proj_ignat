from django.urls import path

from service.views import \
    ServicesApiWithoutOrders, make_order_successful, make_order,\
    OrdersApiForCustomers, OrdersApiForExecutorsWithoutDone, order_page, add_service

urlpatterns = [
    path('service/order-successful/', make_order_successful, name='make_order_successful'),
    path('service/make_order/<slug:service_slug>/', make_order, name='make_order'),
    path('api/service-without-order/<slug:slug>/', ServicesApiWithoutOrders.as_view()),
    path('api/customer-orders/', OrdersApiForCustomers.as_view()),
    path('api/executor-orders/', OrdersApiForExecutorsWithoutDone.as_view()),
    path('service/add_service/', add_service, name='add_service'),
    path('order/<int:order_id>/', order_page, name='order'),

]
