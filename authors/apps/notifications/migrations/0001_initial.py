# Generated by Django 2.1.5 on 2019-01-30 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0015_profile_email_notification_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_status', models.BooleanField(default=False)),
                ('message', models.CharField(max_length=255)),
                ('action_link', models.CharField(max_length=255, null=True)),
                ('email_status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_receiver', to='profiles.Profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile')),
            ],
        ),
    ]
