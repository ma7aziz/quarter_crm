# Generated by Django 3.1.7 on 2021-04-16 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quarter', '0012_auto_20210416_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='notes',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]