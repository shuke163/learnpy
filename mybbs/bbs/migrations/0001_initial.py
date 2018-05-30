# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('url', models.URLField(max_length=255, verbose_name='标题')),
                ('avatar', models.ImageField(height_field=40, upload_to='static/images/', verbose_name='头像', width_field=40)),
                ('summary', models.CharField(max_length=255, verbose_name='简介')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('like_count', models.IntegerField(default=0, verbose_name='点赞数')),
                ('comment_count', models.IntegerField(default=0, verbose_name='评论数')),
            ],
        ),
        migrations.CreateModel(
            name='News2Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='评论的内容')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('new', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.News', verbose_name='评论的新闻ID')),
            ],
        ),
        migrations.CreateModel(
            name='News2Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='点赞的时间')),
                ('new', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.News', verbose_name='点赞的新闻ID')),
            ],
        ),
        migrations.CreateModel(
            name='NewsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=16, verbose_name='标题')),
            ],
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('email', models.EmailField(max_length=16, verbose_name='邮箱')),
            ],
        ),
        migrations.AddField(
            model_name='news2like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.Userinfo', verbose_name='点赞者'),
        ),
        migrations.AddField(
            model_name='news2comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.Userinfo', verbose_name='评论者'),
        ),
        migrations.AddField(
            model_name='news',
            name='commentm2m',
            field=models.ManyToManyField(related_name='commentm2m', through='bbs.News2Comment', to='bbs.Userinfo', verbose_name='评论m2m关系表'),
        ),
        migrations.AddField(
            model_name='news',
            name='new_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.NewsType', verbose_name='新闻类型'),
        ),
        migrations.AddField(
            model_name='news',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bbs.Userinfo', verbose_name='发布者'),
        ),
    ]
