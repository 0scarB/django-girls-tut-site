# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mazes', '0003_auto_20171005_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='maze',
            name='wall_b',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='maze',
            name='wall_g',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='maze',
            name='wall_r',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='maze',
            name='path_b',
            field=models.PositiveSmallIntegerField(default=255),
        ),
        migrations.AlterField(
            model_name='maze',
            name='path_g',
            field=models.PositiveSmallIntegerField(default=255),
        ),
        migrations.AlterField(
            model_name='maze',
            name='path_r',
            field=models.PositiveSmallIntegerField(default=255),
        ),
    ]
