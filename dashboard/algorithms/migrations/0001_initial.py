# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('fabrication_date', models.IntegerField()),
                ('panel', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('max_lifetime', models.IntegerField()),
                ('obsolescence_lifetime', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='technology',
            field=models.ForeignKey(to='algorithms.Technology'),
        ),
    ]
