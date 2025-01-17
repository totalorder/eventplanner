# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-10 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlanningRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=128)),
                ('event_type', models.CharField(max_length=128)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('expected_no_attending', models.IntegerField()),
                ('decoration', models.BooleanField()),
                ('parties', models.BooleanField()),
                ('drinks', models.BooleanField()),
                ('food', models.BooleanField()),
                ('media', models.BooleanField()),
                ('expected_budget', models.IntegerField()),
            ],
        ),
    ]
