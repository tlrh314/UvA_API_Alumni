# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-03 14:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0003_alumnus_survey_info_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumnus',
            name='office',
        ),
        migrations.RemoveField(
            model_name='alumnus',
            name='work_phone',
        ),
    ]
