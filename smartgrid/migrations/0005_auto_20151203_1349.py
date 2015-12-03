# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartgrid', '0004_auto_20151203_1348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='neighbourhood',
            new_name='neighborhood',
        ),
    ]
