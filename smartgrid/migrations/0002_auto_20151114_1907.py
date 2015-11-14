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
            ],
        ),
        migrations.RenameField(
            model_name='consumptionprofile',
            old_name='order',
            new_name='time',
        ),
        migrations.RemoveField(
            model_name='consumptionprofile',
            name='appliance',
        ),
        migrations.RemoveField(
            model_name='consumptionprofile',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='fixeddemand',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='heatloadinvariablepower',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='heatloadvariablepower',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='shiftingloadcycle',
            name='priority',
        ),
        migrations.AddField(
            model_name='consumptionprofile',
            name='shiftingloadcycle',
            field=models.ForeignKey(blank=True, to='smartgrid.ShiftingLoadCycle', null=True),
        ),
        migrations.AddField(
            model_name='onoffprofile',
            name='fixeddemand',
            field=models.ForeignKey(blank=True, to='smartgrid.FixedDemand', null=True),
        ),
        migrations.AddField(
            model_name='onoffprofile',
            name='heatloadinvariablepower',
            field=models.ForeignKey(blank=True, to='smartgrid.HeatLoadInvariablePower', null=True),
        ),
        migrations.AddField(
            model_name='onoffprofile',
            name='heatloadvariablepower',
            field=models.ForeignKey(blank=True, to='smartgrid.HeatLoadVariablePower', null=True),
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
    ]
