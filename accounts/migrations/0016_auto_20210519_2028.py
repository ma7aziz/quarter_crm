# Generated by Django 3.1.7 on 2021-05-19 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210509_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='section',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'مدير الموقع'), (2, 'مدير التركيبات'), (3, 'مدير الصيانة'), (4, 'مشرف كوارتر '), (5, 'مندوب بيع '), (6, 'حسابات'), (7, 'مكتب مصر '), (8, 'فني ')], default=1, verbose_name='الوظيفة'),
        ),
    ]
