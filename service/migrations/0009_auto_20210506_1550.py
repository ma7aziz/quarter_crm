# Generated by Django 3.1.7 on 2021-05-06 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_auto_20210428_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='service_request',
            name='favourite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='service_request',
            name='hold',
            field=models.BooleanField(default=False),
        ),
    ]
