# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_asset_obsolescence_lifetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='fabrication_date',
            new_name='fabrication_year',
        ),
    ]
