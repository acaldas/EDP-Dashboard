# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_parametervalue_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='obsolescence_lifetime',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]
