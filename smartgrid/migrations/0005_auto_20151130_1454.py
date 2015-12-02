# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0004_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fixeddemandprofile',
            name='consumption',
        ),
        migrations.AlterField(
            model_name='heatloadinvariablepower',
            name='id',
            field=models.AutoField(unique=True, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='heatloadvariablepower',
            name='id',
            field=models.AutoField(unique=True, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='current_neighborhood',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='shiftingloadcycle',
            name='id',
            field=models.AutoField(unique=True, serialize=False, primary_key=True),
        ),
    ]
