# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('windopen', '0006_auto_20160821_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 22, 17, 42, 57, 13591)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='action_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 22, 17, 42, 57, 13552)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='close_code',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='last_seen',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 22, 17, 42, 57, 13133)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='open_code',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='registered',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 22, 17, 42, 57, 13023)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='unregistereddevice',
            name='joined',
            field=models.DateTimeField(default=datetime.date(2016, 8, 22)),
            preserve_default=True,
        ),
    ]
