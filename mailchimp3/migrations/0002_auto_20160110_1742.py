# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp3', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='list',
            field=models.ForeignKey(blank=True, to='mailchimp3.List', null=True),
        ),
    ]
