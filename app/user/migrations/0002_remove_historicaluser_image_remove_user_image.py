# Generated by Django 4.1.4 on 2022-12-26 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluser',
            name='image',
        ),
        migrations.RemoveField(
            model_name='user',
            name='image',
        ),
    ]
