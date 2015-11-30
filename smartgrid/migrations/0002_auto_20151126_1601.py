# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='started',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scenario',
            name='time',
            field=models.IntegerField(default=1),
        ),
    ]
