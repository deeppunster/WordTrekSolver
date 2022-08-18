# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 09:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wordtrek', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='animal_name',
            field=models.CharField(help_text='Animal name or "Daily Quest".', max_length=30),
        ),
        migrations.AlterField(
            model_name='animal',
            name='animal_order',
            field=models.IntegerField(default=0, help_text='The sequence number of the animal or "1" for daily quests.'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='category',
            field=models.CharField(choices=[('A', 'Animal'), ('D', 'Daily Quest')], default='A', help_text='Choose either "Animal" or "Daily Quest".', max_length=1),
        ),
        migrations.AlterField(
            model_name='animal',
            name='date_started',
            field=models.DateField(blank=True, default=django.utils.timezone.now, help_text='Please use the following format: <strong>YYYY-MM-DD</strong>.', null=True),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='puzzle_characters',
            field=models.CharField(blank=True, help_text='The letters in the puzzle - left to right, top to bottom.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='puzzle_sequence',
            field=models.IntegerField(default=0, help_text='Puzzle number or sequence of this puzzle.'),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='puzzle_size',
            field=models.IntegerField(default=0, help_text='The number of letters on one side of the puzzle.'),
        ),
    ]