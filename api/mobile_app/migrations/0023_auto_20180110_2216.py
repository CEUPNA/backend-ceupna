# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-10 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_app', '0022_auto_20180110_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='center',
            name='representative_members',
            field=models.ManyToManyField(related_name='center_representatives', through='mobile_app.CenterRepresentative', to='mobile_app.Representative'),
        ),
        migrations.AlterField(
            model_name='department',
            name='representative_members',
            field=models.ManyToManyField(related_name='department_representatives', through='mobile_app.DepartmentRepresentative', to='mobile_app.Representative'),
        ),
    ]
