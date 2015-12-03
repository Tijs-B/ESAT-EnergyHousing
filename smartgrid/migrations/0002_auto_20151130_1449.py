# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='heatloadinvariablepower',
            name='power_consumed',
        ),
        migrations.RemoveField(
            model_name='heatloadvariablepower',
            name='power_consumed',
        ),
        migrations.AddField(
            model_name='fixeddemandprofile',
            name='consumption',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
