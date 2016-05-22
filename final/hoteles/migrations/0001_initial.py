# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-20 06:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(auto_now=True)),
                ('body', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='CSS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.CharField(max_length=32)),
                ('Letra', models.IntegerField()),
                ('Color', models.CharField(default='black', max_length=32)),
                ('Titulo', models.CharField(default='black', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel_selecc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hoteles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=300)),
                ('Categoria', models.CharField(max_length=300)),
                ('estrellas', models.IntegerField()),
                ('Descrip', models.TextField(default='')),
                ('Direc', models.CharField(max_length=120)),
                ('Url', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=120)),
                ('Hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoteles.Hoteles')),
            ],
        ),
        migrations.AddField(
            model_name='hotel_selecc',
            name='Hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoteles.Hoteles'),
        ),
        migrations.AddField(
            model_name='hotel_selecc',
            name='User',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comentario',
            name='Hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoteles.Hoteles'),
        ),
    ]
