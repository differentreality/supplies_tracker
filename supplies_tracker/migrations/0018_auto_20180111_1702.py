# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-11 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplies_tracker', '0017_auto_20180111_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items_storage',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
