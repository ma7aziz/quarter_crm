# Generated by Django 3.1.7 on 2021-04-15 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quarter', '0003_auto_20210414_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='quarter_service',
            name='notes',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]