# Generated by Django 3.2.9 on 2022-03-19 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0004_auto_20220319_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='likes_count',
        ),
        migrations.AddField(
            model_name='news',
            name='likes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='liked_news', to=settings.AUTH_USER_MODEL),
        ),
    ]