# Generated by Django 3.1.7 on 2021-06-18 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quarter', '0002_auto_20210613_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='quarter_service',
            name='favourite',
            field=models.BooleanField(default=False),
        ),
    ]
