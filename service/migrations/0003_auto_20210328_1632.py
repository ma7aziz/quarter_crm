# Generated by Django 3.1.7 on 2021-03-28 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20210328_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_request',
            name='service_type',
            field=models.CharField(choices=[('repair', 'repair'), ('install', 'install')], max_length=10),
        ),
    ]
