# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('italiansushi', '0004_remove_loginprofile_saved_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemset',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 26, 23, 18, 30, 769705, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='itemset',
            name='owner',
            field=models.ForeignKey(to='italiansushi.LoginProfile', null=True),
        ),
    ]
