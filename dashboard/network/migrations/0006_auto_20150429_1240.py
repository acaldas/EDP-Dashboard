# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_asset_parameters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametervalue',
            name='value',
            field=models.ForeignKey(blank=True, to='algorithms.ValueCorrespondence', null=True),
        ),
    ]
