# Generated by Django 2.1.5 on 2019-01-29 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0022_auto_20190129_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='favouriteCount',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
