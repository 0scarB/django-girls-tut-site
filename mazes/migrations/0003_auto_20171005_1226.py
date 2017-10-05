# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mazes', '0002_auto_20171003_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='maze',
            name='horizontal_path_width',
            field=models.DecimalField(decimal_places=4, default=0.5, max_digits=17),
        ),
        migrations.AddField(
            model_name='maze',
            name='horizontal_spacing',
            field=models.PositiveSmallIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='maze',
            name='path_b',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='maze',
            name='path_g',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='maze',
            name='path_r',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='maze',
            name='vertical_spacing',
            field=models.PositiveSmallIntegerField(default=10),
        ),
    ]