# Generated by Django 5.0.7 on 2024-08-12 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quack_app', '0015_alter_user_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_tester',
            field=models.BooleanField(default=False),
        ),
    ]
