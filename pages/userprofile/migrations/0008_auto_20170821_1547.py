# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-21 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_profileabout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileabout',
            name='about_me',
            field=models.TextField(blank=True, verbose_name='About me'),
        ),
    ]
