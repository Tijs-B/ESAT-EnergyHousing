# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0005_auto_20151019_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ivariablepower',
            name='appliance_ptr',
        ),
        migrations.RemoveField(
            model_name='variablepower',
            name='appliance_ptr',
        ),
        migrations.AddField(
            model_name='ivariablepower',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='variablepower',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=2, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
