# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '__first__'),
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParameterValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('value', models.CharField(max_length=200)),
                ('asset', models.ForeignKey(to='network.Asset')),
                ('parameter', models.ForeignKey(to='algorithms.Parameter')),
            ],
        ),
    ]
