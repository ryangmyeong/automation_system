# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-26 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_auto_20181126_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='configtemplate',
            name='template_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
