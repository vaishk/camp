# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-21 09:15
from __future__ import unicode_literals

from django.db import migrations, models
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myfield', markdownx.models.MarkdownxField()),
            ],
        ),
        migrations.AlterField(
            model_name='content',
            name='body',
            field=markdownx.models.MarkdownxField(),
        ),
        migrations.AlterField(
            model_name='content',
            name='header',
            field=markdownx.models.MarkdownxField(),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='camp/static/images'),
        ),
    ]