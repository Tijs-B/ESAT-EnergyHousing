# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0002_auto_20151203_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThermoProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('temp_min', models.FloatField()),
                ('temp_max', models.FloatField()),
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
        ),
        migrations.RemoveField(
            model_name='thermomaxprofile',
            name='house',
        ),
        migrations.RemoveField(
            model_name='thermominprofile',
            name='house',
        ),
        migrations.RemoveField(
            model_name='heatloadvariablepower',
            name='temperature_max_inside',
        ),
        migrations.RemoveField(
            model_name='heatloadvariablepower',
            name='temperature_min_inside',
        ),
        migrations.RemoveField(
            model_name='shiftingloadcycle',
            name='flexibility_end',
        ),
        migrations.RemoveField(
            model_name='shiftingloadcycle',
            name='flexibility_start',
        ),
        migrations.AddField(
            model_name='shiftingloadcycle',
            name='because_there_has_to_be_something',
            field=models.FloatField(default=0),
        ),
        migrations.DeleteModel(
            name='ThermoMaxProfile',
        ),
        migrations.DeleteModel(
            name='ThermoMinProfile',
        ),
    ]
