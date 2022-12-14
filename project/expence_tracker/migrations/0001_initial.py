# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-10-07 02:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseTracker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('category', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500)),
                ('paymentType', models.CharField(max_length=500)),
                ('create_date', models.DateTimeField(default=datetime.datetime(2022, 10, 7, 2, 33, 18, 235560, tzinfo=utc))),
            ],
            options={
                'db_table': 'ExpenseTracker',
            },
        ),
    ]
