# Generated by Django 2.1.5 on 2019-01-17 10:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_profile_some_things'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='some_things',
        ),
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(related_name='is_following', to=settings.AUTH_USER_MODEL),
        ),
    ]
