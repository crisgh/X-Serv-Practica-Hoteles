# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-20 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hoteles',
            old_name='Categoria',
            new_name='categoria',
        ),
        migrations.RenameField(
            model_name='hoteles',
            old_name='Direc',
            new_name='direccion',
        ),
        migrations.RenameField(
            model_name='hoteles',
            old_name='Url',
            new_name='url',
        ),
        migrations.AlterField(
            model_name='hoteles',
            name='estrellas',
            field=models.CharField(max_length=32),
        ),
    ]
