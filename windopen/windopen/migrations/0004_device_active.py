# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('windopen', '0003_auto_20160813_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='active',
            field=models.BooleanField(default=None),
            preserve_default=True,
        ),
    ]
