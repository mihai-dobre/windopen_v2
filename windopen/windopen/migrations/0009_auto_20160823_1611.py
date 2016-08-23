# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('windopen', '0008_auto_20160822_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 23, 16, 11, 11, 413770)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='action_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 23, 16, 11, 11, 413753)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='last_seen',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 23, 16, 11, 11, 413301)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='registered',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 23, 16, 11, 11, 413279)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unregistereddevice',
            name='joined',
            field=models.DateTimeField(default=datetime.date(2016, 8, 23)),
            preserve_default=True,
        ),
    ]
