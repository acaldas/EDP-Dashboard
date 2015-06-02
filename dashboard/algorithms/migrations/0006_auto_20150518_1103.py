# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '0005_auto_20150504_1228'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalFactor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local_weight', models.FloatField()),
                ('global_weight', models.FloatField()),
                ('fault', models.ForeignKey(to='algorithms.Fault')),
                ('parameter', models.ForeignKey(to='algorithms.Parameter')),
            ],
        ),
        migrations.AddField(
            model_name='fault',
            name='external_factors',
            field=models.ManyToManyField(related_name='external_factors', through='algorithms.ExternalFactor', to='algorithms.Parameter'),
        ),
    ]
