# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0007_auto_20151203_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThermoMaxProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('temp_max', models.FloatField()),
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
        ),
        migrations.CreateModel(
            name='ThermoMinProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('temp_min', models.FloatField()),
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
        ),
    ]
