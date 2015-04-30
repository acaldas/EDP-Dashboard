# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_auto_20150430_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametervalue',
            name='value',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
