# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('mailchimp_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_address', models.CharField(max_length=150)),
                ('status', models.CharField(max_length=150, choices=[(b'subscribed', 'Subscribed'), (b'unsubscribed', 'Unsubscribed'), (b'cleaned', 'Cleaned'), (b'pending', 'Pending')])),
                ('mailchimp_id', models.CharField(max_length=50)),
                ('unique_email_id', models.CharField(max_length=50)),
                ('list', models.ForeignKey(to='mailchimp3.List')),
            ],
        ),
    ]
