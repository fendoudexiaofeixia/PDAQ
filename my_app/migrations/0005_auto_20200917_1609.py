# Generated by Django 2.2.16 on 2020-09-17 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_auto_20200916_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdaq',
            name='Set_meal',
            field=models.CharField(default='48G/年', max_length=50, verbose_name='流量卡套餐'),
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '删除'), (1, '正常')], default=1, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='pdaq',
            name='owner',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
    ]