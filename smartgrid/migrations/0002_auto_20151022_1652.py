# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fixeddemand',
            name='room',
        ),
        migrations.AddField(
            model_name='fixeddemand',
            name='room',
            field=models.ForeignKey(default=1, to='smartgrid.Room'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='heatloadinvariablepower',
            name='room',
        ),
        migrations.AddField(
            model_name='heatloadinvariablepower',
            name='room',
            field=models.ForeignKey(default=1, to='smartgrid.Room'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='heatloadvariablepower',
            name='room',
        ),
        migrations.AddField(
            model_name='heatloadvariablepower',
            name='room',
            field=models.ForeignKey(default=1, to='smartgrid.Room'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='shiftingloadcycle',
            name='room',
        ),
        migrations.AddField(
            model_name='shiftingloadcycle',
            name='room',
            field=models.ForeignKey(default=1, to='smartgrid.Room'),
            preserve_default=False,
        ),
    ]
