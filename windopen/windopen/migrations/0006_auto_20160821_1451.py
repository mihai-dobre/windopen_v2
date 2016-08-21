# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('windopen', '0005_auto_20160821_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='device',
            field=models.ForeignKey(to='windopen.Device', to_field=b'uuid'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='uuid',
            field=models.CharField(unique=True, max_length=128),
            preserve_default=True,
        ),
    ]
