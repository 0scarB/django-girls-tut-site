# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mazes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maze',
            name='text',
        ),
        migrations.AddField(
            model_name='maze',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='maze',
            name='width',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
