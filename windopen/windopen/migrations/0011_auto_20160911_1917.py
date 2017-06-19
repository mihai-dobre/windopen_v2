# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('windopen', '0010_auto_20160825_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 11, 19, 17, 19, 317836)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='action_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 11, 19, 17, 19, 317820)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='last_seen',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 11, 19, 17, 19, 317374)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='registered',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 11, 19, 17, 19, 317355)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unregistereddevice',
            name='joined',
            field=models.DateTimeField(default=datetime.date(2016, 9, 11)),
            preserve_default=True,
        ),
    ]
