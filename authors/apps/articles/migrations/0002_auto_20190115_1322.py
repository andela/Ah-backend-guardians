# Generated by Django 2.1.5 on 2019-01-15 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleimg',
            name='article',
        ),
        migrations.RemoveField(
            model_name='article',
            name='likes_count',
        ),
        migrations.RemoveField(
            model_name='article',
            name='read_count',
        ),
        migrations.RemoveField(
            model_name='article',
            name='read_time',
        ),
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='article',
            name='view_count',
        ),
        migrations.DeleteModel(
            name='ArticleImg',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
