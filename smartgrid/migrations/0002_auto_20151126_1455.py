# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='current_neighborhood',
            field=models.ForeignKey(to='smartgrid.Neighborhood'),
        ),
    ]
