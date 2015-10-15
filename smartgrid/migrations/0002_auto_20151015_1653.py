# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heatload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appliance', models.ForeignKey(to='smartgrid.Appliance')),
            ],
        ),
        migrations.CreateModel(
            name='Ivariablepower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temprange', models.CharField(default=b'C', max_length=2, choices=[(b'VC', b'T<-10'), (b'C', b'T<0'), (b'N', b'0<T<20'), (b'H', b'T>20')])),
                ('powerrange', models.CharField(default=b'M', max_length=2, choices=[(b'VL', b'50'), (b'L', b'100'), (b'M', b'200'), (b'H', b'500'), (b'VH', b'1000')])),
                ('heatload', models.ForeignKey(to='smartgrid.Heatload')),
            ],
        ),
        migrations.CreateModel(
            name='Variablepower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temprange', models.CharField(default=b'C', max_length=2, choices=[(b'VC', b'T<-10'), (b'C', b'T<0'), (b'N', b'0<T<20'), (b'H', b'T>20')])),
                ('powerrange', models.CharField(default=b'M', max_length=2, choices=[(b'VL', b'1-50'), (b'L', b'50-100'), (b'M', b'100-200'), (b'H', b'200-500'), (b'VH', b'500-1000')])),
                ('heatload', models.ForeignKey(to='smartgrid.Heatload')),
            ],
        ),
        migrations.RenameField(
            model_name='house',
            old_name='neighbourhood',
            new_name='neighborhood',
        ),
    ]
