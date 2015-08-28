# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('italiansushi', '0008_auto_20150828_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemset',
            name='users_upvotes',
            field=models.ManyToManyField(default=None, related_name='users_who_upvoted', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
