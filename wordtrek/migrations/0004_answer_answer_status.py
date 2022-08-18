# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 01:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordtrek', '0003_answerletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answer_status',
            field=models.CharField(choices=[('U', 'Unsolved'), ('H', 'Hinted'), ('S', 'Solved')], default='U', help_text='Is this answer unsolved, hinted, or solved?', max_length=1),
        ),
    ]
