# Generated by Django 2.2.16 on 2020-09-22 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0005_auto_20200917_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdaq',
            name='owner',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='建者'),
        ),
    ]