# Generated by Django 3.2.9 on 2021-12-29 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20211221_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
