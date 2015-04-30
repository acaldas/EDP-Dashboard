# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('aging_function', models.ForeignKey(to='utils.RegressionFunction', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('asset', models.ForeignKey(to='algorithms.AssetType')),
            ],
        ),
        migrations.CreateModel(
            name='Fault',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('global_weight', models.FloatField()),
                ('local_weight', models.FloatField()),
                ('condition_weight', models.FloatField()),
                ('age_weight', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('component', models.ForeignKey(to='algorithms.Component')),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('fault', models.ForeignKey(to='algorithms.Fault')),
                ('function', models.ForeignKey(blank=True, to='utils.RegressionFunction', null=True)),
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
            options={
                'verbose_name_plural': 'Technologies',
            },
        ),
        migrations.CreateModel(
            name='ValueCorrespondence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=200)),
                ('health_index', models.FloatField()),
                ('warning', models.CharField(max_length=200, null=True, blank=True)),
                ('alert', models.CharField(max_length=200, null=True, blank=True)),
                ('parameter', models.ForeignKey(to='algorithms.Parameter')),
            ],
        ),
        migrations.AddField(
            model_name='fault',
            name='function',
            field=models.ForeignKey(to='algorithms.Function'),
        ),
        migrations.AddField(
            model_name='assettype',
            name='technology',
            field=models.ForeignKey(to='algorithms.Technology'),
        ),
    ]
