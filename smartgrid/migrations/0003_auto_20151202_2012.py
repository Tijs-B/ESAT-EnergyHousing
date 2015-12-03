# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0002_auto_20151130_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recording',
            name='sensor',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='power_capacity',
            new_name='total_power_capacity',
        ),
        migrations.AddField(
            model_name='sensor',
            name='value',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Recording',
        ),
    ]
