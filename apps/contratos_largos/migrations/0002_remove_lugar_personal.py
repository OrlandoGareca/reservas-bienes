# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-06-12 19:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratos_largos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lugar',
            name='personal',
        ),
    ]