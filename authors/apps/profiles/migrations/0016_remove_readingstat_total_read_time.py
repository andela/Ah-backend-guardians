# Generated by Django 2.1.5 on 2019-01-29 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_readingstat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readingstat',
            name='total_read_time',
        ),
    ]