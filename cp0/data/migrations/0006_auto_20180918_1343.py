# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-09-18 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20180905_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='OS_version',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='project',
            name='board_type',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='project',
            name='build_label',
            field=models.CharField(default='', max_length=30),
        ),
    ]