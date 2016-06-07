# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-23 21:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bioinfuse', '0009_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='subm_start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de d\xe9but de soumission'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='subm_stop_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de fin de soumission'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='subs_start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date de d\xe9but d'inscription"),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='subs_stop_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date de fin d'inscription"),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_url',
            field=models.URLField(null=True, verbose_name='Lien vers la vid\xe9o'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='submit_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='La date doit \xeatre ins\xe9r\xe9e sous forme jj/mm/aaaa hh:mm:ss', verbose_name='Date de soumission'),
        ),
    ]
