# Generated by Django 3.1.7 on 2021-05-18 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quarter', '0022_auto_20210518_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='status',
            field=models.CharField(choices=[(1, 'approved'), (2, 'pending'), (3, 'rejected')], default='pending', max_length=15),
        ),
        migrations.AlterField(
            model_name='price',
            name='status',
            field=models.CharField(choices=[(1, 'approved'), (2, 'pending'), (3, 'rejected')], default='pending', max_length=15),
        ),
    ]