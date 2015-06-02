# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '0007_auto_20150519_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technology',
            name='aging_parameters',
        ),
        migrations.AddField(
            model_name='parameter',
            name='technology',
            field=models.ForeignKey(blank=True, to='algorithms.Technology', null=True),
        ),
    ]
