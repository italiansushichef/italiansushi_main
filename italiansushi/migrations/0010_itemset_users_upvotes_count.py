# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('italiansushi', '0009_auto_20150828_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemset',
            name='users_upvotes_count',
            field=models.IntegerField(default=0),
        ),
    ]
