# Generated by Django 2.1.5 on 2019-01-30 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_profile_email_notification_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_notification_permissions',
            field=models.BooleanField(default=True),
        ),
    ]