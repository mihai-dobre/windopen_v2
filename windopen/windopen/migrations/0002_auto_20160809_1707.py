# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('windopen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=128)),
                ('action_start', models.DateTimeField(default=datetime.date(2016, 8, 9))),
                ('action_end', models.DateTimeField(default=datetime.date(2016, 8, 9))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=128)),
                ('open_code', models.CharField(max_length=32)),
                ('close_code', models.CharField(max_length=32)),
                ('registered', models.DateTimeField(default=datetime.date(2016, 8, 9))),
                ('last_seen', models.DateTimeField(default=datetime.date(2016, 8, 9))),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnregisteredDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=32)),
                ('joined', models.DateTimeField(default=datetime.date(2016, 8, 9))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='dropboxprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='DropboxProfile',
        ),
        migrations.RemoveField(
            model_name='facebookprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='FacebookProfile',
        ),
        migrations.RemoveField(
            model_name='foursquareprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='FoursquareProfile',
        ),
        migrations.RemoveField(
            model_name='githubprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='GithubProfile',
        ),
        migrations.RemoveField(
            model_name='googleprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='GoogleProfile',
        ),
        migrations.RemoveField(
            model_name='instagramprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='InstagramProfile',
        ),
        migrations.RemoveField(
            model_name='linkedinprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='LinkedinProfile',
        ),
        migrations.DeleteModel(
            name='MeetupToken',
        ),
        migrations.DeleteModel(
            name='Snippet',
        ),
        migrations.RemoveField(
            model_name='tumblrprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='TumblrProfile',
        ),
        migrations.RemoveField(
            model_name='twitterprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='TwitterProfile',
        ),
        migrations.AddField(
            model_name='action',
            name='device',
            field=models.ForeignKey(to='windopen.Device'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
