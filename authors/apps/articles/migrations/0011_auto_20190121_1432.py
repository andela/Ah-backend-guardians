# Generated by Django 2.1.5 on 2019-01-21 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_article_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='images',
            field=models.CharField(max_length=255),
        ),
    ]