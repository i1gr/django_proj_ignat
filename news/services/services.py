# I don't know how to name this python file :((((((((
from random import randrange

from django.utils.text import slugify

from news.models import NewsComments
from users.models import Profile


def get_unique_slug(instance, slug=None):
    if slug:
        slug += str(randrange(10))
    else:
        slug = slugify(instance.title)

    if is_slug_unique(instance, slug):
        return slug

    return get_unique_slug(instance, slug)


def is_slug_unique(instance, slug):
    obj = type(instance).objects.filter(slug=slug)
    if obj:
        return False
    return True


def get_user_from_instance(user_instance):
    obj = Profile.objects.get(email=user_instance.email)
    print(obj)
    print(obj.id)
    print(type(obj))
    return obj


def change_stars_grading(news_instance):
    comments = NewsComments.objects.filter(news=news_instance)
    if comments:
        stars = 0
        for comment in comments:
            stars += comment.stars

    news_instance.stars = round(stars/len(comments), 2)
    news_instance.save()
