# Question
# QuerySet has been imported for TypeHints. Is it normal? or maybe i can use typehints without import some libs?
from django.db.models import QuerySet, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from service.forms import OrderForm
from service.models import Services, Orders
from rest_framework import generics

from service.serializer import ServicesSerializerWithoutOrders, OrdersSerializer


def make_order_successful(request):
    return render(request, 'service/make_order_successful.html', {'title': 'Successful order', 'nav_active': 'None'})


def make_order(request, service_slug):
    service_data = get_object_or_404(Services, slug=service_slug)
    user = request.user

    if not user.is_authenticated:
        return redirect(to='login')

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.name = service_data.name
            order.service = service_data
            order.customer = user
            order.save()
            return redirect('make_order_successful')
    else:
        form = OrderForm()

    context = {
        'title': f'{service_data.name}',
        'nav_active': 'None',
        'service_data': service_data,
        'form': form,
    }

    return render(request, 'service/make_order.html', context=context)


class ServicesApiWithoutOrders(generics.RetrieveAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializerWithoutOrders
    lookup_field = 'slug'


class OrdersApiForCustomers(generics.ListAPIView):
    serializer_class = OrdersSerializer

    def get_queryset(self) -> QuerySet | None:
        current_user = self.request.user
        if current_user.is_authenticated:
            return Orders.objects.filter(customer=current_user)
        return None


class OrdersApiForExecutors(generics.ListAPIView):
    serializer_class = OrdersSerializer

    def get_queryset(self) -> QuerySet | None:
        current_user = self.request.user
        if current_user.is_authenticated:
            return Orders.objects.filter(~Q(koban_type="DN") & (Q(executor=current_user) | Q(executor=None)))
        return None
