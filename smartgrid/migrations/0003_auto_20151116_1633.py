# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0002_auto_20151114_1907'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixedDemandProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('consumption', models.FloatField()),
                ('fixeddemand', models.ForeignKey(to='smartgrid.FixedDemand')),
            ],
        ),
        migrations.AlterField(
            model_name='consumptionprofile',
            name='shiftingloadcycle',
            field=models.ForeignKey(default=1, to='smartgrid.ShiftingLoadCycle'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shiftingloadcycle',
            name='flexibility_end',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='shiftingloadcycle',
            name='flexibility_start',
            field=models.TimeField(),
        ),
    ]
