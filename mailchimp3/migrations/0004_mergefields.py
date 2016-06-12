# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp3', '0003_auto_20160114_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='MergeFields',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=100)),
                ('member', models.ForeignKey(to='mailchimp3.Member')),
            ],
        ),
    ]
