# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp3', '0004_mergefields'),
    ]

    operations = [
        migrations.CreateModel(
            name='MergeField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=100)),
                ('member', models.ForeignKey(to='mailchimp3.Member')),
            ],
        ),
        migrations.RemoveField(
            model_name='mergefields',
            name='member',
        ),
        migrations.DeleteModel(
            name='MergeFields',
        ),
    ]
