# Generated by Django 3.2.9 on 2022-03-19 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20220319_1512'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='likes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.news'),
        ),
    ]