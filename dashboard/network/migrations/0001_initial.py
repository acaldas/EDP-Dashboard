# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('fabrication_date', models.IntegerField()),
                ('panel', models.CharField(max_length=200, null=True, blank=True)),
                ('asset_type', models.ForeignKey(to='algorithms.AssetType')),
            ],
        ),
    ]
