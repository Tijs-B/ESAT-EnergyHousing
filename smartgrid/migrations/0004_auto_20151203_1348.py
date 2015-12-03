# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0003_auto_20151202_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='neighborhood',
            name='power_consumed',
        ),
        migrations.AddField(
            model_name='heatloadinvariablepower',
            name='power_consumed',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='heatloadvariablepower',
            name='power_consumed',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
