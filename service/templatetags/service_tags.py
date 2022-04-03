from django import template

from service.models import Orders

register = template.Library()


@register.simple_tag()
def is_user_read(user, instance: Orders) -> bool:
    """Return:
        True if user read last comments in the instance,
            False if user doesn't read last comments,
                and if user is staff and somebody make order.
    """
    if instance.is_read:
        return True

    order_comments = list(instance.ordercomments_set.all())
    last_comment = None
    if order_comments:
        last_comment = order_comments[0]

    if last_comment is None and user.is_staff:
        return False
    elif last_comment is None and not user.is_staff:
        return True
    elif last_comment.author == user:
        return True
    return False