# Generated by Django 2.1.5 on 2019-01-30 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0023_auto_20190129_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favourites',
            old_name='author',
            new_name='user',
        ),
    ]
