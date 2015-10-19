# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableEnergy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('solar', models.FloatField(default=0)),
                ('wind', models.FloatField(default=0)),
                ('other', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ConsumptionProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='FixedDemand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appliance_name', models.CharField(max_length=200)),
                ('priority', models.IntegerField(default=0, choices=[(0, b'Low'), (1, b'Normal'), (2, b'High'), (3, b'Very High')])),
                ('currently_on', models.BooleanField(default=False)),
                ('consumption', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HeatLoadInvariablePower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appliance_name', models.CharField(max_length=200)),
                ('priority', models.IntegerField(default=0, choices=[(0, b'Low'), (1, b'Normal'), (2, b'High'), (3, b'Very High')])),
                ('currently_on', models.BooleanField(default=False)),
                ('temperature_min', models.FloatField()),
                ('temperature_max', models.FloatField()),
                ('power', models.FloatField()),
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
                ('priority', models.IntegerField(default=0, choices=[(0, b'Low'), (1, b'Normal'), (2, b'High'), (3, b'Very High')])),
                ('currently_on', models.BooleanField(default=False)),
                ('temperature_min', models.FloatField()),
                ('temperature_max', models.FloatField()),
                ('power_min', models.FloatField()),
                ('power_max', models.FloatField()),
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
                ('energy_price', models.FloatField(default=1)),
                ('neighborhood_name', models.CharField(max_length=200)),
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
                ('priority', models.IntegerField(default=0, choices=[(0, b'Low'), (1, b'Normal'), (2, b'High'), (3, b'Very High')])),
                ('currently_on', models.BooleanField(default=False)),
                ('flexibility_start', models.DateTimeField()),
                ('flexibility_end', models.DateTimeField()),
                ('room', models.ForeignKey(to='smartgrid.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='recording',
            name='sensor',
            field=models.ForeignKey(to='smartgrid.Sensor'),
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
            model_name='fixeddemand',
            name='room',
            field=models.ForeignKey(to='smartgrid.Room'),
        ),
        migrations.AddField(
            model_name='consumptionprofile',
            name='appliance',
            field=models.ForeignKey(to='smartgrid.ShiftingLoadCycle'),
        ),
        migrations.AddField(
            model_name='availableenergy',
            name='neighborhood',
            field=models.ForeignKey(to='smartgrid.Neighborhood'),
        ),
    ]
