# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-09-16 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoodwatch', '0011_auto_20190916_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='neighimage/'),
        ),
    ]
