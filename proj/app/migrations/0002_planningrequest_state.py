# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-10 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='planningrequest',
            name='state',
            field=models.CharField(choices=[('new', 'New'), ('cso_approved', 'CSO Approved'), ('fm_commented', 'FM Commented')], default='new', max_length=15),
        ),
    ]
