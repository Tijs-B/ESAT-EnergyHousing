# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0006_totalconsumption'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalculatedConsumption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('total_consumption', models.FloatField()),
                ('house', models.ForeignKey(to='smartgrid.House')),
            ],
        ),
        migrations.RemoveField(
            model_name='totalconsumption',
            name='house',
        ),
        migrations.DeleteModel(
            name='TotalConsumption',
        ),
    ]
