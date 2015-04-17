# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_auto_20150417_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regressionfunction',
            name='type',
            field=models.IntegerField(default=1, choices=[(1, b'Linear'), (2, b'Exponencial'), (3, b'Quadr\xe1tica 2\xba Grau'), (4, b'Quadr\xe1tica 3\xba Grau')]),
        ),
    ]
