# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '0008_auto_20150519_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technology',
            name='obsolescence_lifetime',
        ),
    ]
