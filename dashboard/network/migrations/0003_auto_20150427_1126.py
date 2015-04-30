# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_parametervalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametervalue',
            name='value',
            field=models.ForeignKey(to='algorithms.ValueCorrespondence'),
        ),
    ]
