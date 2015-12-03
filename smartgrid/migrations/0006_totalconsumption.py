# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0005_auto_20151203_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalConsumption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('total_consumption', models.FloatField()),
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
        ),
    ]
