# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('windopen', '0007_auto_20160822_1742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='action',
            options={'ordering': ['action_start']},
        ),
        migrations.AddField(
            model_name='device',
            name='status',
            field=models.CharField(default=b'close', max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='action_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 22, 18, 32, 35, 64836)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='action_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 22, 18, 32, 35, 64820)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='last_seen',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 22, 18, 32, 35, 64299)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='registered',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 22, 18, 32, 35, 64274)),
            preserve_default=True,
        ),
    ]
