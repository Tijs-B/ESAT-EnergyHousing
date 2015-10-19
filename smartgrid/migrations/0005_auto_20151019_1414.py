# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0004_appliance_appliance_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ivariablepower',
            name='id',
        ),
        migrations.RemoveField(
            model_name='variablepower',
            name='id',
        ),
        migrations.AddField(
            model_name='ivariablepower',
            name='appliance_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default='koelkast', serialize=False, to='smartgrid.Appliance'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variablepower',
            name='appliance_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default='koelkast', serialize=False, to='smartgrid.Appliance'),
            preserve_default=False,
        ),
    ]
