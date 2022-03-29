import django
from django.db.models import Q

from service.models import Orders


def get_choices_from_query(model: django.db.models.base.ModelBase, filter_params: dict) -> list:
    """Return choices list for select widget from model by filter"""

    query = model.objects.filter(**filter_params)
    choices = list()

    for q in query:
        choices.append((q.pk, str(q)))

    return choices


def is_user_read(user, instance: Orders) -> bool:
    """Return:
        True if user read last comments in the instance,
            False if user doesn't read last comments,
                and if user is staff and somebody make order.
    """
    if instance.is_read:
        return True

    last_comment = instance.ordercomments_set.all().order_by('-datetime').first()

    if last_comment is None and user.is_staff:
        return False
    elif last_comment is None and not user.is_staff:
        return True
    elif last_comment.author == user:
        return True
    return False


def get_notifications_count(user) -> dict:
    """Return count of user unread comments in Orders"""

    if not user.is_authenticated:
        return {}

    if user.is_staff:
        queryset = Orders.objects.filter((Q(executor=user) | Q(executor=None) | Q(customer=user)) & Q(is_read=False))
    else:
        queryset = Orders.objects.filter(Q(customer=user) & Q(is_read=False))

    count = len(queryset)

    for instance in queryset:

        if is_user_read(user, instance):
            count -= 1

    return {"notifications_count": count}


def make_read(user, instance: Orders) -> None:
    """Make order field is read True"""

    if not is_user_read(user, instance):
        instance.is_read = True
        instance.save()


def make_unread(instance: Orders) -> None:
    """Make order field is read False"""

    instance.is_read = False
    instance.save()
