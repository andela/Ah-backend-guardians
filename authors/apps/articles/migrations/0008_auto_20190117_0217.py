# Generated by Django 2.1.5 on 2019-01-17 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20190116_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='articles', to='articles.Tag'),
        ),
    ]