# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('italiansushi', '0002_auto_20150822_0330'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemset',
            name='name',
            field=models.CharField(default=b'noname.json', max_length=32),
        ),
    ]
