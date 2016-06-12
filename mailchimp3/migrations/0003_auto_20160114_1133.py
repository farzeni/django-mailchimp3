# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailchimp3', '0002_auto_20160110_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseChimpModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='list',
            name='id',
        ),
        migrations.RemoveField(
            model_name='member',
            name='id',
        ),
        migrations.AddField(
            model_name='list',
            name='basechimpmodel_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=None, serialize=False, to='mailchimp3.BaseChimpModel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='basechimpmodel_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=None, serialize=False, to='mailchimp3.BaseChimpModel'),
            preserve_default=False,
        ),
    ]
