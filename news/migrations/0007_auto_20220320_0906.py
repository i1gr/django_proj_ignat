# Generated by Django 3.2.9 on 2022-03-20 09:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0006_rename_likes_news_users_who_liked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='users_who_liked',
        ),
        migrations.AddField(
            model_name='news',
            name='users_who_liked',
            field=models.ManyToManyField(null=True, related_name='liked_news', to=settings.AUTH_USER_MODEL),
        ),
    ]
