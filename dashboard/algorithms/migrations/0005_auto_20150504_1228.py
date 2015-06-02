# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '0004_auto_20150430_1649'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parameters',
            options={'verbose_name_plural': 'Parameters'},
        ),
    ]
