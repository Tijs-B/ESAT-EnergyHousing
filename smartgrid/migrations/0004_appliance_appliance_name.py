# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0003_room_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliance',
            name='appliance_name',
            field=models.CharField(default='droogkast', max_length=200),
            preserve_default=False,
        ),
    ]
