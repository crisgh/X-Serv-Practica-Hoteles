# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-23 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0009_auto_20160522_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='Nombre_comentario',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
    ]
