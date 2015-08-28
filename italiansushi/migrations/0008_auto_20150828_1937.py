# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('italiansushi', '0007_auto_20150828_0258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='itemset',
            name='users_upvotes',
            field=models.ManyToManyField(default=None, related_name='users_who_upvoted', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='itemset',
            name='owner',
            field=models.ForeignKey(related_name='owner_of_itemset', default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.DeleteModel(
            name='LoginProfile',
        ),
    ]
