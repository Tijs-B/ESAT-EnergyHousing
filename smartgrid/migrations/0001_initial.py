# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AmbientTemp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('temperature', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='AvailableEnergy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='CalculatedConsumption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('total_consumption', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('car_name', models.CharField(max_length=200)),
                ('total_power_capacity', models.IntegerField()),
                ('load_capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EnergyPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='FixedDemandProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('consumption', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='HeatLoadInvariablePower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appliance_name', models.CharField(max_length=200)),
                ('power_required', models.FloatField()),
                ('isolation_coefficient', models.FloatField()),
                ('coefficient_of_performance', models.FloatField()),
                ('mass_of_air', models.FloatField()),
                ('temperature_min_inside', models.FloatField()),
                ('temperature_max_inside', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HeatLoadVariablePower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appliance_name', models.CharField(max_length=200)),
                ('power_required', models.FloatField()),
                ('isolation_coefficient', models.FloatField()),
                ('coefficient_of_performance', models.FloatField()),
                ('mass_of_air', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('house_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('neighborhood_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='OnOffInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('on_off', models.IntegerField(default=0)),
                ('info', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OnOffProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('car', models.ForeignKey(blank=True, to='smartgrid.Car', null=True)),
                ('heatloadinvariablepower', models.ForeignKey(blank=True, to='smartgrid.HeatLoadInvariablePower', null=True)),
                ('heatloadvariablepower', models.ForeignKey(blank=True, to='smartgrid.HeatLoadVariablePower', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_name', models.CharField(max_length=200)),
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scenario_name', models.CharField(max_length=200)),
                ('current_neighborhood', models.CharField(max_length=200)),
                ('time', models.IntegerField(default=1)),
                ('started', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sensor_name', models.CharField(max_length=200)),
                ('value', models.FloatField()),
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
        ),
        migrations.CreateModel(
            name='ShiftingLoadCycle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appliance_name', models.CharField(max_length=200)),
                ('because_there_has_to_be_something', models.FloatField(default=0)),
                ('room', models.ForeignKey(to='smartgrid.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShiftingLoadProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('consumption', models.FloatField()),
                ('shiftingloadcycle', models.ForeignKey(to='smartgrid.ShiftingLoadCycle')),
            ],
        ),
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
        migrations.AddField(
            model_name='onoffprofile',
            name='shiftingloadcycle',
            field=models.ForeignKey(blank=True, to='smartgrid.ShiftingLoadCycle', null=True),
        ),
        migrations.AddField(
            model_name='onoffinfo',
            name='onoffprofile',
            field=models.ForeignKey(to='smartgrid.OnOffProfile'),
        ),
        migrations.AddField(
            model_name='house',
            name='neighborhood',
            field=models.ForeignKey(to='smartgrid.Neighborhood'),
        ),
        migrations.AddField(
            model_name='heatloadvariablepower',
            name='room',
            field=models.ForeignKey(to='smartgrid.Room'),
        ),
        migrations.AddField(
            model_name='heatloadinvariablepower',
            name='room',
            field=models.ForeignKey(to='smartgrid.Room'),
        ),
        migrations.AddField(
            model_name='fixeddemandprofile',
            name='house',
            field=models.ForeignKey(to='smartgrid.House'),
        ),
        migrations.AddField(
            model_name='energyprice',
            name='neighborhood',
            field=models.ForeignKey(to='smartgrid.Neighborhood'),
        ),
        migrations.AddField(
            model_name='car',
            name='house',
            field=models.ForeignKey(to='smartgrid.House'),
        ),
        migrations.AddField(
            model_name='calculatedconsumption',
            name='house',
            field=models.ForeignKey(to='smartgrid.House'),
        ),
        migrations.AddField(
            model_name='availableenergy',
            name='neighborhood',
            field=models.ForeignKey(to='smartgrid.Neighborhood'),
        ),
        migrations.AddField(
            model_name='ambienttemp',
            name='neighborhood',
            field=models.ForeignKey(to='smartgrid.Neighborhood'),
        ),
    ]
