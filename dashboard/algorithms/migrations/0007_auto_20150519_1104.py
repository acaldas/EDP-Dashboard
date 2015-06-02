# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '0006_auto_20150518_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faults',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'Faults',
            },
            bases=('algorithms.fault',),
        ),
        migrations.AddField(
            model_name='technology',
            name='aging_parameters',
            field=models.ManyToManyField(to='algorithms.Parameter'),
        ),
    ]
