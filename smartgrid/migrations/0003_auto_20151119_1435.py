# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smartgrid', '0002_auto_20151119_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('house', models.ForeignKey(to='smartgrid.House')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='fuckinguserregistration',
            name='house',
        ),
        migrations.RemoveField(
            model_name='fuckinguserregistration',
            name='user',
        ),
        migrations.DeleteModel(
            name='FuckingUserRegistration',
        ),
    ]
