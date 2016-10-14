# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 10:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_financialrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruitmentrequest',
            name='completed',
        ),
        migrations.AddField(
            model_name='recruitmentrequest',
            name='state',
            field=models.CharField(choices=[('new', 'New'), ('approved', 'Approved'), ('denied', 'Denied')], default='new', max_length=15),
        ),
    ]