# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordtrek', '0007_auto_20170323_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_text', models.CharField(max_length=255)),
                ('show_hide', models.CharField(choices=[('s', 'Show'), ('h', 'Hide')], default='s', help_text='Choose to show or hide this word', max_length=1)),
            ],
            options={
                'ordering': ['word_text'],
            },
        ),
    ]