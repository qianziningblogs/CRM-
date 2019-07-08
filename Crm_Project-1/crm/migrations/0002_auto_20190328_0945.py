# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-03-28 01:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(blank=True, to='rbac.Role', verbose_name='用户所拥有的角色'),
        ),
        migrations.AlterField(
            model_name='consultrecord',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='crm.UserProfile', verbose_name='销售'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='class_list',
            field=models.ManyToManyField(blank=True, to='crm.ClassList', verbose_name='已报班级'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Campuses', verbose_name='校区'),
        ),
    ]
