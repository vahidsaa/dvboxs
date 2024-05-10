import datetime
from django.db import models

# Create your models here.

class TodayList(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام')
    status = models.CharField(max_length=50, verbose_name=' وضعیت ساخت')
    send = models.CharField(max_length=50, verbose_name='وضعیت ارسال')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'لیست تحویل'


class Today(models.Model):
    today_date = models.DateField(default=datetime.datetime.today)
    date = models.CharField(max_length=60, verbose_name='امروز')

    def __str__(self):
        return self.date

    class Meta:
        verbose_name_plural = 'تاریخ تحویل'