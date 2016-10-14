# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_planningrequest_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='planningrequest',
            name='budget_feedback',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='planningrequest',
            name='state',
            field=models.CharField(choices=[('new', 'New'), ('cso_approved', 'CSO Approved'), ('scso_approved', 'SCSO Approved'), ('fm_commented', 'FM Commented'), ('adm_approved', 'ADM Approved')], default='new', max_length=15),
        ),
    ]
