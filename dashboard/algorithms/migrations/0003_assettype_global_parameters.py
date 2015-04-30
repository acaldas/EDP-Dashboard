# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '0002_globalparameter'),
    ]

    operations = [
        migrations.AddField(
            model_name='assettype',
            name='global_parameters',
            field=models.ManyToManyField(to='algorithms.Parameter', through='algorithms.GlobalParameter'),
        ),
    ]
