from django.db import models
from django.urls import reverse

from users.models import Profile


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True,)
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    users_who_liked = models.ManyToManyField(Profile, related_name='liked_news', blank=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return str(self.title) + '\n\t' + str(self.text)

    def get_absolute_url(self):
        return reverse(viewname='article', kwargs={'article_slug': self.slug})


class NewsComments(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=1)
    text = models.TextField()
    news = models.ForeignKey(News, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return str(self.text)


