# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regressionfunction',
            name='type',
            field=models.CharField(default=b'LI', max_length=2, choices=[(b'LI', b'Linear'), (b'EX', b'Exponencial'), (b'Q2', b'Quadr\xe1tica 2\xba Grau'), (b'Q3', b'Quadr\xe1tica 3\xba Grau')]),
        ),
    ]
