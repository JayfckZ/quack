# Generated by Django 5.0.7 on 2024-08-11 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quack_app', '0014_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]