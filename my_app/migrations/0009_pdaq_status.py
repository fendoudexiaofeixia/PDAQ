# Generated by Django 2.2.16 on 2020-09-24 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0008_auto_20200924_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdaq',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, '正常'), (0, '维修'), (2, '损坏')], default=1, verbose_name='设备状态'),
        ),
    ]