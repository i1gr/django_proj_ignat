import csv
from django.core.mail import EmailMessage
from io import StringIO

from service.models import Orders
from users.models import Profile


def send_email_to_staff():
    SUBJECT = 'New Order'
    BODY = 'We have new order!'
    EMAIL = 'notification@umbrella.com'

    orders = _get_all_orders_data_for_staff()

    staff = Profile.objects.filter(is_staff=True)
    staffs_email = list(map(lambda user: user.email, staff))

    csv_file = StringIO()
    fieldnames = ['name', 'kanban', 'customer', 'executor']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(orders)

    email = EmailMessage(
        SUBJECT,
        BODY,
        EMAIL,
        [staffs_email],
    )
    email.attach('all_orders.csv', csv_file.getvalue(), 'text/csv')
    email.send()


def send_email_to_customer(user_id: int):
    SUBJECT = 'You make order'
    BODY = 'Thanks!\n' \
           'You are the best❤️'
    EMAIL = 'notification@umbrella.com'

    user = Profile.objects.get(id=user_id)
    body = 'Hello ' + user.username + '!\n' + BODY

    orders = _get_orders_data_for_customer(user_id)

    csv_file = StringIO()
    fieldnames = ['name', 'kanban', 'executor']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(orders)

    email = EmailMessage(
        SUBJECT,
        body,
        EMAIL,
        [user.email],
    )
    email.attach('all_orders.csv', csv_file.getvalue(), 'text/csv')
    email.send()


def _get_all_orders_data_for_staff() -> list:
    queryset = Orders.objects.exclude(kanban_type='AR') \
        .select_related('service', 'customer', 'executor')

    orders = []
    for order in queryset:
        executor = 'None'
        if order.executor:
            executor = str(order.executor)

        order_data = {
            'name': order.name,
            'kanban': order.kanban_type,
            'customer': str(order.customer),
            'executor': executor,
        }
        orders.append(order_data)
    return orders


def _get_orders_data_for_customer(user_id: int) -> list:
    queryset = Orders.objects.filter(customer=user_id).select_related('service', 'executor')

    orders = []
    for order in queryset:
        executor = 'None'
        if order.executor:
            executor = order.executor.username

        order_data = {
            'name': order.name,
            'kanban': order.kanban_type,
            'executor': executor,
        }
        orders.append(order_data)
    return orders
