# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '__first__'),
        ('network', '0004_auto_20150427_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='parameters',
            field=models.ManyToManyField(to='algorithms.Parameter', through='network.ParameterValue'),
        ),
    ]
