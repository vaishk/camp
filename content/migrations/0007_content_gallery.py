# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-19 13:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0010_auto_20160105_1307'),
        ('content', '0006_auto_20171219_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='gallery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content', to='photologue.Gallery'),
        ),
    ]
