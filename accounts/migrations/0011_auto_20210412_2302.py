# Generated by Django 3.1.7 on 2021-04-12 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210325_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favourite_count',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='id',
            field=models.PositiveIntegerField(choices=[(1, 'جميع الأقسام'), (2, 'التركيب'), (3, 'الصيانة'), (4, 'كوارتر ')], primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'مدير الموقع'), (2, 'مشرف'), (3, 'فني'), (4, 'مندوب بيع'), (5, 'تسعير'), (6, 'حسابات'), (7, 'مشتريات'), (8, 'الرسم'), (9, 'التنفيذ')], default=1, verbose_name='الوظيفة'),
        ),
    ]