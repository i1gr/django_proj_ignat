from random import randrange

from django.core.exceptions import ValidationError
from django.db.models.base import ModelBase
from django.utils.text import slugify

from news.models import NewsComments
from users.models import Profile


def get_unique_slug(instance: ModelBase, field_to_slug_gen: str, slug=None) -> str:
    """Return unique slug. field_to_slug_gen is the field that is used to generate slug"""
    if slug:
        slug += str(randrange(10))
    else:
        slug = slugify(field_to_slug_gen)

    if _is_slug_unique(instance, slug):
        return slug

    return get_unique_slug(instance, slug)


def _is_slug_unique(instance: ModelBase, slug: str) -> bool:
    obj = type(instance).objects.filter(slug=slug)
    if obj:
        return False
    return True


def get_clean_title(title: str) -> str:
    """Return cleaned title or raise ValidationError <The first word must start with a letter or number.>"""
    title = title.strip()

    if title[0].isalnum():
        title = title[0].upper() + title[1:]
        return title
    raise ValidationError('The first word must start with a letter or number.')


def get_user_from_instance(user_instance):
    obj = Profile.objects.get(email=user_instance.email)
    return obj


def change_stars_grading(news_instance):
    comments = NewsComments.objects.filter(news=news_instance)
    if comments:
        stars = 0
        for comment in comments:
            stars += comment.stars

    news_instance.stars = round(stars/len(comments), 2)
    news_instance.save()
