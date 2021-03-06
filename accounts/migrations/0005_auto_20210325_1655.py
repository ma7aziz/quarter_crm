# Generated by Django 3.1.7 on 2021-03-25 14:55

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210322_1726'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'admin'), (2, 'supervisor'), (3, 'technician'), (4, 'sales')], default=1, verbose_name='الوظيفة'),
        ),
    ]
