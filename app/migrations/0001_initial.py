# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-13 01:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAnalysisImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pa_img_url', models.ImageField(upload_to='static/uploads/')),
            ],
            options={
                'verbose_name_plural': '图片分析',
                'db_table': 'product_analysis_image',
            },
        ),
        migrations.CreateModel(
            name='ProductCommentTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_c_time', models.CharField(blank=True, max_length=32, null=True, verbose_name='产品评论日期')),
            ],
            options={
                'verbose_name_plural': '评论日期',
                'db_table': 'product_comment_time',
            },
        ),
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_url', models.CharField(max_length=256, verbose_name='产品url')),
                ('p_title', models.CharField(max_length=32, verbose_name='产品名称')),
                ('p_img', models.CharField(max_length=256, verbose_name='产品图片')),
                ('p_id', models.IntegerField(verbose_name='产品ID')),
                ('p_prices', models.CharField(blank=True, max_length=128, null=True, verbose_name='商品价格')),
                ('p_c_score', models.FloatField(blank=True, null=True, verbose_name='产品总评分')),
                ('p_comments', models.CharField(blank=True, max_length=128, null=True, verbose_name='产品评价')),
                ('p_c_all_nums', models.CharField(blank=True, max_length=256, null=True, verbose_name='概况点评内容')),
            ],
            options={
                'verbose_name_plural': '产品信息',
                'db_table': 'product_info',
            },
        ),
        migrations.AddField(
            model_name='productcommenttime',
            name='p_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ProductInfo', verbose_name='所属产品'),
        ),
        migrations.AddField(
            model_name='productanalysisimage',
            name='p_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ProductInfo', verbose_name='所属产品'),
        ),
    ]