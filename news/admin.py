from django.contrib import admin
from news.models import News, NewsComments

# Register your models here.
admin.site.register(News)
admin.site.register(NewsComments)