# Generated by Django 4.1.7 on 2023-03-27 11:17

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_install_user_repair'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
    ]