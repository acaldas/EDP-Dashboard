# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FunctionValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RegressionFunction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'LIN', max_length=2, choices=[(b'LIN', b'Linear'), (b'EXP', b'Exponencial'), (b'Q2', b'Quadr\xe1tica 2\xba Grau'), (b'Q3', b'Quadr\xe1tica 3\xba Grau')])),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='functionvalue',
            name='function',
            field=models.ForeignKey(to='utils.RegressionFunction'),
        ),
    ]
