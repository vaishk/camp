# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-19 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_auto_20171219_1311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='fil',
            new_name='file',
        ),
        migrations.AlterField(
            model_name='content',
            name='shortname',
            field=models.CharField(db_column='shortName', max_length=255, unique=True, verbose_name='Slug'),
        ),
    ]
