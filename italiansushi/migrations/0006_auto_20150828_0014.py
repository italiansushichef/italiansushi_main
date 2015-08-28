# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('italiansushi', '0005_auto_20150826_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemset',
            name='champ_against',
            field=models.CharField(default=b'', max_length=32),
        ),
        migrations.AddField(
            model_name='itemset',
            name='champ_for',
            field=models.CharField(default=b'', max_length=32),
        ),
        migrations.AddField(
            model_name='itemset',
            name='lane',
            field=models.CharField(default=b'', max_length=1, choices=[(b'M', b'mid'), (b'T', b'top'), (b'B', b'bot'), (b'J', b'jungle'), (b'', b'any')]),
        ),
    ]
