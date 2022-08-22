# Generated by Django 2.0.3 on 2018-05-25 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordtrek', '0009_auto_20171225_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='category',
            field=models.CharField(choices=[('A', 'Animal'), ('D', 'Daily&nbsp;Quest'), ('Z', 'Other')], default='A', help_text='Choose either "Animal" or "Daily Quest".', max_length=1),
        ),
    ]
