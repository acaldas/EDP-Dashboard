# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20150429_1240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parametervalue',
            old_name='value',
            new_name='value_interval',
        ),
    ]
