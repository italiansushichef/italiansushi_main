# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('italiansushi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemset',
            name='users',
        ),
        migrations.AddField(
            model_name='itemset',
            name='owner',
            field=models.ForeignKey(default=None, to='italiansushi.LoginProfile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='loginprofile',
            name='saved_count',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
