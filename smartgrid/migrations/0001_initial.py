# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appliance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField(default=0, choices=[(0, b'Low'), (1, b'Normal'), (2, b'High'), (3, b'Very High')])),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('energy_price', models.FloatField()),
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
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
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
            model_name='appliance',
            name='room',
            field=models.ForeignKey(to='smartgrid.Room'),
        ),
    ]
