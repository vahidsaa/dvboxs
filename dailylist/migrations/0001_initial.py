# Generated by Django 5.0.4 on 2024-04-12 09:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Today',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('today_date', models.DateField(default=datetime.datetime.today)),
                ('date', models.CharField(max_length=60, verbose_name='امروز')),
            ],
            options={
                'verbose_name_plural': 'تاریخ تحویل',
            },
        ),
        migrations.CreateModel(
            name='TodayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='نام')),
                ('status', models.CharField(max_length=50, verbose_name=' وضعیت ساخت')),
                ('send', models.CharField(max_length=50, verbose_name='وضعیت ارسال')),
            ],
            options={
                'verbose_name_plural': 'لیست تحویل',
            },
        ),
    ]
