# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-22 03:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swagger', '0004_auto_20180322_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='type',
            field=models.CharField(choices=[('string', 'string'), ('integer', 'integer'), ('object', 'object'), ('array', 'array'), ('boolean', 'boolean')], default='string', max_length=45),
        ),
    ]
