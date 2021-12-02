from django.db import models
from users.models import Profile


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True,)
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    stars = models.FloatField()
    comments = models.ForeignKey('NewsComments', on_delete=models.CASCADE, related_name='+')

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return str(self.title) + '\n\t' + str(self.text)


class NewsComments(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    stars = models.IntegerField()
    news = models.OneToOneField(News, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-datetime"]

    def __str__(self):
        return str(self.title) + '\n\t' + str(self.text)

