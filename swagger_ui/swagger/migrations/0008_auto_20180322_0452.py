# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-22 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swagger', '0007_auto_20180322_0422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='description',
            field=models.TextField(),
        ),
    ]
