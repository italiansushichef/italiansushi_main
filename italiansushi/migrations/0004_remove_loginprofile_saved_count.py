# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('italiansushi', '0003_itemset_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginprofile',
            name='saved_count',
        ),
    ]
