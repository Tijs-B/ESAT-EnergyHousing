# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiftingloadcycle',
            name='car_current_charge',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='shiftingloadcycle',
            name='car_min_charge',
            field=models.FloatField(blank=True),
        ),
    ]
