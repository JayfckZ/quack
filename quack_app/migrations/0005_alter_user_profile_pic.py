# Generated by Django 5.0.7 on 2024-08-05 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quack_app', '0004_user_followers_user_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/'),
        ),
    ]
