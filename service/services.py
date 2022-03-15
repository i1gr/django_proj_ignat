import django
from django.db.models import Q


def get_choices_from_query(model: django.db.models.base.ModelBase, filter_params: dict) -> list:
    """Return choices list for select widget from model by filter"""

    query = model.objects.filter(**filter_params)
    choices = list()

    for q in query:
        choices.append((q.pk, str(q)))

    return choices
