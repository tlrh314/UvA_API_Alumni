# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 18:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobAfterLeaving',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=100, verbose_name='Company Name')),
                ('position_name', models.CharField(blank=True, max_length=100, verbose_name='Position Name')),
                ('is_inside_academia', models.PositiveSmallIntegerField(choices=[(1, 'Yes'), (2, 'No')], default=1, verbose_name='In Academia')),
                ('location_job', django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='Location')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='From')),
                ('stop_date', models.DateField(blank=True, null=True, verbose_name='Until')),
                ('which_position', models.PositiveSmallIntegerField(choices=[(0, 'Current'), (1, 'First'), (2, 'Second'), (3, 'Third')], default=0, verbose_name='Which position')),
                ('comments', models.TextField(blank=True, verbose_name='comments')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Last Changed')),
                ('show_job', models.BooleanField(default=True, verbose_name='Show job on personal page')),
                ('alumnus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobs_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job After Leaving API',
                'verbose_name_plural': 'Jobs After Leaving API',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Last Changed')),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sectors_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Job Sector',
                'verbose_name_plural': 'Job Sectors',
            },
        ),
        migrations.AddField(
            model_name='jobafterleaving',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.Sector'),
        ),
    ]