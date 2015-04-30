# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '0003_assettype_global_parameters'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parameters',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('algorithms.parameter',),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='fault',
            field=models.ForeignKey(blank=True, to='algorithms.Fault', null=True),
        ),
    ]
