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
                ('currently_on', models.BooleanField(default=False)),
                ('power_required', models.FloatField()),
                ('isolation_coefficient', models.FloatField()),
                ('coefficient_of_performance', models.FloatField()),
                ('mass_of_air', models.FloatField()),
                ('power_consumed', models.FloatField()),
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
                ('currently_on', models.BooleanField(default=False)),
                ('power_required', models.FloatField()),
                ('isolation_coefficient', models.FloatField()),
                ('coefficient_of_performance', models.FloatField()),
                ('mass_of_air', models.FloatField()),
                ('power_consumed', models.FloatField()),
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
                ('power_consumed', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OnOffInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('OnOff', models.IntegerField(default=0)),
                ('Info', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OnOffProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heatloadinvariablepower', models.ForeignKey(blank=True, to='smartgrid.HeatLoadInvariablePower', null=True)),
                ('heatloadvariablepower', models.ForeignKey(blank=True, to='smartgrid.HeatLoadVariablePower', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('timestamp', models.DateTimeField()),
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
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sensor_name', models.CharField(max_length=200)),
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
        ),
        migrations.CreateModel(
            name='ShiftingLoadCycle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appliance_name', models.CharField(max_length=200)),
                ('currently_on', models.BooleanField(default=False)),
                ('flexibility_start', models.TimeField()),
                ('flexibility_end', models.TimeField()),
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
        migrations.AddField(
            model_name='recording',
            name='sensor',
            field=models.ForeignKey(to='smartgrid.Sensor'),
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
            name='neighbourhood',
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
