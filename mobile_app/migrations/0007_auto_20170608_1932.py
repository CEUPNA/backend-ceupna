# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-08 17:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_app', '0006_auto_20170420_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('upna_id', models.PositiveIntegerField(unique=True)),
                ('name_es', models.CharField(blank=True, default='', max_length=150)),
                ('name_eus', models.CharField(blank=True, default='', max_length=150)),
                ('name_en', models.CharField(blank=True, default='', max_length=150)),
                ('url', models.CharField(blank=True, default='', max_length=200)),
                ('bachelor', models.BooleanField(default=False)),
                ('international_prog', models.BooleanField(default=False)),
                ('english_prog', models.BooleanField(default=False)),
                ('french_prog', models.BooleanField(default=False)),
                ('last_updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('upna_id', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('credits', models.FloatField(default=0)),
                ('year', models.IntegerField(default=0)),
                ('semester', models.IntegerField(default=0)),
                ('type', models.CharField(blank=True, default='', max_length=2)),
                ('language', models.CharField(blank=True, default='', max_length=3)),
                ('department', models.CharField(blank=True, default='', max_length=100)),
                ('evaluation', models.CharField(blank=True, default='', max_length=10000)),
                ('contents', models.CharField(blank=True, default='', max_length=10000)),
                ('curriculum', models.CharField(blank=True, default='', max_length=10000)),
                ('last_updated', models.DateField(auto_now=True)),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobile_app.Degree')),
            ],
        ),
        migrations.RenameField(
            model_name='center',
            old_name='name',
            new_name='name_es',
        ),
        migrations.AddField(
            model_name='center',
            name='name_en',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='center',
            name='name_eus',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='telephone',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='subject',
            name='teachers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobile_app.Teacher'),
        ),
        migrations.AddField(
            model_name='degree',
            name='center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobile_app.Center'),
        ),
    ]
