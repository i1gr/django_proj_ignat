from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet, Q, Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from news.services.services import get_unique_slug
from service.forms import OrderForm, KanbanSelectForm, ExecutorSelectForm, AddServiceForm, OrderCommentsForm, \
    QuestionForm
from service.models import Services, Orders, OrderComments
from rest_framework import generics, filters

from service.serializer import ServicesSerializerWithoutOrders, OrdersSerializer
from service.services import make_read, make_unread, get_notifications_count
from service.tasks import send_mails_after_order


def make_order_successful(request):
    context = dict()

    context.update(get_notifications_count(request.user))
    context.update({'title': 'Successful order', 'nav_active': 'None'})

    return render(request, 'service/make_order_successful.html', context=context)


def make_order(request, service_slug):
    service_data = get_object_or_404(Services, slug=service_slug)
    user = request.user
    context = dict()
    order_form = None
    question_form = None

    context.update(get_notifications_count(user))

    if request.method == "POST":
        if not user.is_authenticated:
            return redirect(to='login')
        order_form = OrderForm(request.POST)
        question_form = QuestionForm(request.POST)

        if order_form.is_valid() and 'order_button' in request.POST:
            order = order_form.save(commit=False)
            order.service = service_data
            order.customer = user
            order.save()
            order.name = str(service_data.name) + ' #' + str(order.pk)
            order.save()
            send_mails_after_order.delay(request.user.id)
            return redirect('make_order_successful')

        if question_form.is_valid() and 'question_button' in request.POST:
            question = question_form.save(commit=False)
            question.service = service_data
            question.customer = user
            question.save()
            question.name = 'Question: ' + str(service_data.name) + ' #' + str(question.pk)
            question.save()
            return redirect('messages')
    else:
        order_form = OrderForm()
        question_form = QuestionForm()

    context.update({
        'title': f'{service_data.name}',
        'nav_active': 'None',
        'service_data': service_data,
        'order_form': order_form,
        'question_form': question_form,
        'block_content': 'full_screen',
    })

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

    def get_queryset(self) -> QuerySet:
        current_user = self.request.user
        if current_user.is_staff:
            return Orders.objects.filter(
                ~Q(kanban_type="DN") & ~Q(kanban_type="AR") & (Q(executor=current_user) | Q(executor=None))) \
                .select_related('executor', 'customer')
        raise PermissionDenied


class OrdersApiKanbanAll(generics.ListAPIView):
    serializer_class = OrdersSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self) -> QuerySet:
        current_user = self.request.user
        if current_user.is_staff:
            return Orders.objects.all()
        raise PermissionDenied


class OrdersApiKanbanForCustomer(generics.ListAPIView):
    serializer_class = OrdersSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self) -> QuerySet:
        current_user = self.request.user
        if current_user.is_authenticated:
            return Orders.objects.filter(customer=current_user)
        raise PermissionDenied


class OrdersApiKanbanForExecutor(generics.ListAPIView):
    serializer_class = OrdersSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self) -> QuerySet:
        current_user = self.request.user
        if current_user.is_staff:
            return Orders.objects.filter(executor=current_user)
        raise PermissionDenied


def order_page(request, order_id):
    order_data = get_object_or_404(
        Orders.objects.select_related('executor', 'customer').prefetch_related(
            Prefetch('ordercomments_set',
                     queryset=OrderComments.objects.all().order_by('-datetime').select_related('author'))),
        pk=order_id)
    comments_data = order_data.ordercomments_set.all().select_related('author')

    user = request.user
    make_read(user, order_data)
    context = dict()

    context.update(get_notifications_count(user))

    kanban_form = None
    executor_form = None
    comment_form = None

    if not user.is_authenticated:
        return redirect(to='login')
    if user != order_data.customer and not user.is_staff:
        return redirect(to='home')

    match request.method:
        case 'POST':
            comment_form = OrderCommentsForm(request.POST)

            if user.is_staff:
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

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = user
                comment.order = order_data
                comment.save()
                make_unread(order_data)
                return redirect(to=order_data)
        case _:
            if user.is_staff:
                kanban_form = KanbanSelectForm(order_data)
                executor_form = ExecutorSelectForm(user)
            comment_form = OrderCommentsForm()

    ''' 
    vs 
    
    if request.method == "POST":
        comment_form = OrderCommentsForm(request.POST)

        if user.is_staff:
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

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = user
            comment.order = order_data
            comment.save()
            make_unread(order_data)
            return redirect(to=order_data)
    else:
        if user.is_staff:
              kanban_form = KanbanSelectForm(order_data)
              executor_form = ExecutorSelectForm(user)
        comment_form = OrderCommentsForm()
    '''

    context.update({
        'title': f'{order_data.name}',
        'nav_active': 'None',
        'order_data': order_data,
        'comments_data': comments_data,
        'kanban_form': kanban_form,
        'executor_form': executor_form,
        'comment_form': comment_form,
        'block_content': 'full_screen',
    })

    return render(request, 'service/order.html', context=context)


def add_service(request):
    if not request.user.is_staff:
        raise PermissionDenied

    context = dict()

    context.update(get_notifications_count(request.user))

    if request.method == "POST":
        form = AddServiceForm(request.POST)

        if form.is_valid():
            new_service = form.save(commit=False)
            new_service.slug = get_unique_slug(new_service, new_service.name)
            new_service.save()
            return redirect('home')
    else:
        form = AddServiceForm()

    context.update({
        'title': "Add service",
        'nav_active': 'None',
        'form': form,
    })
    return render(request, 'service/add_service.html', context=context)


def services(request):
    services_queryset = Services.objects.all()
    context = dict()
    
    context.update(get_notifications_count(request.user))
    context.update({"title": 'Services', 'nav_active': 'services', 'services': services_queryset})
    return render(request, 'service/services.html', context=context)


def messages(request):
    user = request.user
    context = dict()
    queryset = None

    if not user.is_authenticated:
        return redirect(to='login')

    if user.is_staff:
        queryset = Orders.objects.filter(Q(executor=user) | Q(executor=None))
    if not user.is_staff:
        queryset = Orders.objects.filter(customer=user)

    context.update(get_notifications_count(user))
    context.update({"title": 'Messages', 'nav_active': 'messages', 'messages': queryset})
    return render(request, 'service/messages.html', context=context)


class MessagesListView(ListView):
    model = Orders
    context_object_name = 'messages'
    template_name = 'service/messages.html'

    extra_context = {"title": 'Messages', 'nav_active': 'messages'}
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_notifications_count(self.request.user))
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = None
        if user.is_staff:
            queryset = Orders.objects.filter(customer=user).prefetch_related(
                Prefetch('ordercomments_set',
                         queryset=OrderComments.objects.all().order_by('-datetime').select_related(
                             'author'))).select_related('customer')
        if not user.is_staff:
            queryset = Orders.objects.filter(customer=user).prefetch_related(
                Prefetch('ordercomments_set',
                         queryset=OrderComments.objects.all().order_by('-datetime').select_related(
                             'author'))).select_related('executor')
        return queryset
