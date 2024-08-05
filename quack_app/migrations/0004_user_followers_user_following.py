# Generated by Django 5.0.7 on 2024-08-05 16:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quack_app', '0003_alter_user_handle'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='user_following', to=settings.AUTH_USER_MODEL),
        ),
    ]
