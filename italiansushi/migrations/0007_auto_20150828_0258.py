# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('italiansushi', '0006_auto_20150828_0014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemset',
            name='champ_against',
        ),
        migrations.AddField(
            model_name='itemset',
            name='champ_against',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='itemset',
            name='champ_for',
        ),
        migrations.AddField(
            model_name='itemset',
            name='champ_for',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
