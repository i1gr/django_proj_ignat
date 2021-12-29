from django.contrib import admin
from news.models import News, NewsComments


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


# Register your models here.
admin.site.register(News, NewsAdmin)
admin.site.register(NewsComments)
