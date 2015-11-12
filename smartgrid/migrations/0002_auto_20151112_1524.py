# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0001_initial'),
    ]

    operations = [
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
                ('fixeddemand', models.ForeignKey(blank=True, to='smartgrid.FixedDemand', null=True)),
                ('heatloadinvariablepower', models.ForeignKey(blank=True, to='smartgrid.HeatLoadInvariablePower', null=True)),
                ('heatloadvariablepower', models.ForeignKey(blank=True, to='smartgrid.HeatLoadVariablePower', null=True)),
                ('shiftingloadcycle', models.ForeignKey(blank=True, to='smartgrid.ShiftingLoadCycle', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='onoffinfo',
            name='onoffprofile',
            field=models.ForeignKey(to='smartgrid.OnOffProfile'),
        ),
    ]
