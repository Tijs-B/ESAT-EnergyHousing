# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0002_auto_20151015_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='house_name',
            field=models.CharField(default=b'Huisje', max_length=200),
        ),
    ]
