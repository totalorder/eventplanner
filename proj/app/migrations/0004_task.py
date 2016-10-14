# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 09:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20161014_0904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('extra_needs', models.TextField()),
                ('sub_team', models.CharField(choices=[('video_photo', 'Video and photography unit'), ('audio', 'Audio unit'), ('graphics', 'Graphics unit'), ('decoration', 'Decoration unit'), ('network', 'Networking unit'), ('food', 'Food unit'), ('waiters', 'Waiter staff')], max_length=128)),
                ('planning_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='app.PlanningRequest')),
            ],
        ),
    ]