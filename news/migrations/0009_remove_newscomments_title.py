# Generated by Django 3.2.9 on 2022-03-28 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_news_users_who_liked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newscomments',
            name='title',
        ),
    ]
