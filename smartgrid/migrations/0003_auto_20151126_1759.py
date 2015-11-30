# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0002_auto_20151126_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('car_name', models.CharField(max_length=200)),
                ('power_capacity', models.IntegerField()),
                ('load_capacity', models.IntegerField()),
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
        ),
        migrations.AddField(
            model_name='heatloadinvariablepower',
            name='temperature_max_inside',
            field=models.FloatField(default=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='heatloadinvariablepower',
            name='temperature_min_inside',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='heatloadvariablepower',
            name='temperature_max_inside',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='heatloadvariablepower',
            name='temperature_min_inside',
            field=models.FloatField(default=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='onoffprofile',
            name='car',
            field=models.ForeignKey(blank=True, to='smartgrid.Car', null=True),
        ),
    ]
