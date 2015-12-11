# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shiftingloadcycle',
            name='because_there_has_to_be_something',
        ),
        migrations.AddField(
            model_name='availableenergy',
            name='wind',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shiftingloadcycle',
            name='latest_end_time',
            field=models.IntegerField(default=72),
            preserve_default=False,
        ),
    ]
