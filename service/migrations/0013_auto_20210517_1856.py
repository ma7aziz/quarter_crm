# Generated by Django 3.1.7 on 2021-05-17 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0012_service_request_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hold_reason',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
