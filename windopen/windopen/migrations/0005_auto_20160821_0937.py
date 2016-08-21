# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('windopen', '0004_device_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_end',
            field=models.DateTimeField(default=datetime.date(2016, 8, 21)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='action_start',
            field=models.DateTimeField(default=datetime.date(2016, 8, 21)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='last_seen',
            field=models.DateTimeField(default=datetime.date(2016, 8, 21)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='registered',
            field=models.DateTimeField(default=datetime.date(2016, 8, 21)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unregistereddevice',
            name='joined',
            field=models.DateTimeField(default=datetime.date(2016, 8, 21)),
            preserve_default=True,
        ),
    ]
