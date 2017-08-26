# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 05:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('leader', models.CharField(max_length=16)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32, unique=True)),
                ('private_ip', models.GenericIPAddressField(null=True)),
                ('public_ip', models.GenericIPAddressField(null=True, unique=True)),
                ('os', models.CharField(default='ubuntu 16.04', max_length=16)),
                ('cpu', models.CharField(max_length=10)),
                ('mem', models.CharField(max_length=16)),
                ('disk', models.CharField(max_length=16)),
                ('owner', models.CharField(max_length=32, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idc', models.CharField(max_length=16)),
                ('regionId', models.CharField(max_length=16)),
                ('area', models.CharField(max_length=32)),
                ('owner', models.CharField(max_length=16)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service2hosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='host.Hosts')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('owner', models.CharField(max_length=16)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('include_idc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='host.Idc')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=32)),
                ('sex', models.BooleanField(choices=[(0, '男'), (1, '女')], max_length=1)),
                ('email', models.EmailField(max_length=32)),
                ('phone', models.CharField(max_length=16)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('dep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='host.Department')),
            ],
        ),
        migrations.AddField(
            model_name='service2hosts',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='host.Services'),
        ),
        migrations.AddField(
            model_name='hosts',
            name='idc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='host.Idc'),
        ),
        migrations.AddField(
            model_name='hosts',
            name='service',
            field=models.ManyToManyField(through='host.Service2hosts', to='host.Services'),
        ),
        migrations.AddField(
            model_name='hosts',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='host.Status'),
        ),
    ]