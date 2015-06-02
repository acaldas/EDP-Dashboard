# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '0010_auto_20150602_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assettype',
            name='technology',
            field=models.OneToOneField(to='algorithms.Technology'),
        ),
    ]
