# Generated by Django 2.1.5 on 2019-01-15 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='images/avatar/'),
        ),
    ]