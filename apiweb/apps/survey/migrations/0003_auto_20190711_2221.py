# Generated by Django 2.2.3 on 2019-07-11 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_jobafterleaving_is_inside_astronomy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobafterleaving',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='survey.Sector'),
        ),
        migrations.AlterField(
            model_name='jobafterleaving',
            name='show_job',
            field=models.BooleanField(blank=True, default=True, verbose_name='Show job on personal page'),
        ),
    ]