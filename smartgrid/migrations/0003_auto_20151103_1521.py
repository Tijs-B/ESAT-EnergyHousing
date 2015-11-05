# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0002_auto_20151103_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiftingloadcycle',
            name='car_current_charge',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='shiftingloadcycle',
            name='car_min_charge',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
