# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20150427_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametervalue',
            name='value',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
