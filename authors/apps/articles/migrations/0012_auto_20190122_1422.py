# Generated by Django 2.1.5 on 2019-01-22 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0011_auto_20190121_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='article',
            name='images',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
