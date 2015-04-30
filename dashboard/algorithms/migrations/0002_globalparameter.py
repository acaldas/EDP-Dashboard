# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local_weight', models.FloatField()),
                ('global_weight', models.FloatField()),
                ('asset', models.ForeignKey(to='algorithms.AssetType')),
                ('parameter', models.ForeignKey(to='algorithms.Parameter')),
            ],
        ),
    ]
