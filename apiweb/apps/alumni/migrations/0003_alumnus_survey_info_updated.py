# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 01:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0002_auto_20170720_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumnus',
            name='survey_info_updated',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date survey info updated'),
        ),
    ]