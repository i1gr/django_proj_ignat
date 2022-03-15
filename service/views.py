from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet, Q
from django.shortcuts import render, get_object_or_404, redirect

from news.services.services import get_unique_slug
from service.forms import OrderForm, KanbanSelectForm, ExecutorSelectForm, AddServiceForm
from service.models import Services, Orders
from rest_framework import generics, filters

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
            order.service = service_data
            order.customer = user
            order.save()
            # ????????????????????????????????????????????
            order.name = str(service_data.name) + ' #' + str(order.pk)
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
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self) -> QuerySet | None:
        current_user = self.request.user
        if current_user.is_authenticated:
            return Orders.objects.filter(customer=current_user)
        return None


class OrdersApiForExecutorsWithoutDone(generics.ListAPIView):
    serializer_class = OrdersSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = None

    def get_queryset(self) -> QuerySet | None:
        current_user = self.request.user
        if current_user.is_staff:
            return Orders.objects.filter(~Q(kanban_type="DN") & (Q(executor=current_user) | Q(executor=None))) \
                .select_related('executor', 'customer')
        return None


class OrdersApiKanbanDone(generics.ListAPIView):
    serializer_class = OrdersSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'

    def get_queryset(self) -> QuerySet | None:
        current_user = self.request.user
        if current_user.is_authenticated:
            return Orders.objects.filter(kanban_type="DN")
        return None


def order_page(request, order_id):
    order_data = get_object_or_404(Orders.objects.select_related('executor', 'customer'), pk=order_id)
    user = request.user
    kanban_form = None
    executor_form = None

    if not user.is_authenticated:
        return redirect(to='login')
    if user != order_data.customer and not user.is_staff:
        return redirect(to='home')

    if user.is_staff:
        if request.method == "POST":
            kanban_form = KanbanSelectForm(order_data, request.POST)
            executor_form = ExecutorSelectForm(user, request.POST)

            if kanban_form.is_valid():
                order_data.kanban_type = kanban_form.cleaned_data['kanban_type']
                order_data.save()
                return redirect(to=order_data)

            if executor_form.is_valid():
                order_data.executor = executor_form.cleaned_data['executor']
                order_data.save()
                return redirect(to=order_data)
        else:
            kanban_form = KanbanSelectForm(order_data)
            executor_form = ExecutorSelectForm(user)

    context = {
        'title': f'{order_data.name}',
        'nav_active': 'None',
        'order_data': order_data,
        'kanban_form': kanban_form,
        'executor_form': executor_form,
    }

    return render(request, 'service/order.html', context=context)


def add_service(request):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == "POST":
        form = AddServiceForm(request.POST)

        if form.is_valid():
            new_service = form.save(commit=False)
            new_service.slug = get_unique_slug(new_service, new_service.name)
            new_service.save()
            return redirect('home')
    else:
        form = AddServiceForm()

    context = {
        'title': "Add service",
        'nav_active': 'None',
        'form': form,
    }
    return render(request, 'service/add_service.html', context=context)
