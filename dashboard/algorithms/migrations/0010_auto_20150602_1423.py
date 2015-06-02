# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithms', '0009_remove_technology_obsolescence_lifetime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parameter',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='parameters',
            options={'ordering': ('name',), 'verbose_name_plural': 'Parameters'},
        ),
        migrations.AlterModelOptions(
            name='technology',
            options={'ordering': ('name',), 'verbose_name_plural': 'Technologies'},
        ),
        migrations.AlterField(
            model_name='parameter',
            name='fault',
            field=models.ForeignKey(blank=True, editable=False, to='algorithms.Fault', null=True),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='technology',
            field=models.ForeignKey(blank=True, editable=False, to='algorithms.Technology', null=True),
        ),
    ]
