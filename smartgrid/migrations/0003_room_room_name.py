# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0002_auto_20151015_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_name',
            field=models.CharField(default='keuken', max_length=200),
            preserve_default=False,
        ),
    ]
