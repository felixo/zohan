# Encoding: utf-8
from django.contrib.sessions.models import Session

import datetime
from django.db import models
from django.db.models import Q
from dateutil.relativedelta import relativedelta

class DayStatus(models.Model):
    WORKDAY = 0
    OFFDAY = 1
    CATERING = 2
    SALON = 3

    STATUS_CHOICES = (
        (WORKDAY, u'Рабочий день'),
        (OFFDAY, u'Выходной'),
        (CATERING, u'Только выезд'),
        (SALON, u'Только салон'),
    )

    date = models.DateField(unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=WORKDAY)

    @classmethod
    def get_status_for_day(cls, date):
        try:
            return cls.objects.get(date=date).status
        except cls.DoesNotExist:
            return cls.WORKDAY


        
class CrossingEntryException(Exception):
    pass


class Record(models.Model):
    name = models.CharField(verbose_name=u'Имя', max_length=128)
    catering  = models.BooleanField(verbose_name=u'Выезд на дом', default=True, null=False)
    address = models.TextField(verbose_name=u'Ваш адрес и контактный телефон', max_length=128)
    email = models.CharField(verbose_name=u'Электронная почта', max_length=128)

    man_haircut = models.BooleanField(verbose_name=u'Мужская стрижка', default=False, null=False)
    woman_haircut = models.BooleanField(verbose_name=u'Женская стрижка', default=False, null=False)
    coloring = models.BooleanField(verbose_name=u'Окрашивание', default=False, null=False)
    haircare = models.BooleanField(verbose_name=u'Уход', default=False, null=False)
    laminate = models.BooleanField(verbose_name=u'Ламинирование', default=False, null=False)

    comment = models.TextField(verbose_name=u'Комментарий', blank=True)
    metro = models.CharField(verbose_name=u'Станция Метро', max_length=32, default='')

    start = models.DateTimeField(verbose_name=u'Начало', null=False)
    end = models.DateTimeField(verbose_name=u'Окончание', null=False)

    session_id = models.CharField(max_length=40, default="")


    def updateTime(self):
        if self.id:
            return False
        end = self.start
        if self.man_haircut:
            end += datetime.timedelta(hours=1)
        if self.woman_haircut:
            end += datetime.timedelta(hours=1, minutes=30)
        if self.coloring:
            end += datetime.timedelta(hours=1, minutes=30)
        if self.haircare:
            end += datetime.timedelta(minutes=30)
        if self.laminate:
            end += datetime.timedelta(hours=1)
        if self.catering:
            self.start -= datetime.timedelta(minutes=30)
        self.end = end


    def get_title(self):
        title = u''
        services = []
        if self.man_haircut:
            services.append(u'мужская стрижка')
        if self.woman_haircut:
            services.append(u'женская стрижка')
        if self.coloring:
            services.append(u'окрашивание')
        if self.coloring:
            services.append(u'уход')

        where = u'с выездом %s м. ' % self.metro if self.catering else u'без выезда'

        return u'%s. %s %s' % (self.name, u', '.join(services), where)

    
    def save(self, *agrs, **kwargs):
        crossing_records = Record.objects.filter(
            Q(start__lte=self.start, end__gt=self.start) |
            Q(start__lt=self.end, end__gte=self.end) |
            Q(start__lte=self.start, end__gte=self.end) |
            Q(start__gte=self.start, end__lte=self.end)
        ).exclude(id=self.id)
        if crossing_records.count():
            message = u'К сожалению ваша запись с %s до %s пересекается с другой записью с %s до %s \nПожалуйста выберите другое время.' 
            record = crossing_records[0]
            message%= (self.start.strftime('%H:%M'), self.end.strftime('%H:%M'), record.start.strftime('%H:%M'), record.end.strftime('%H:%M'))
            raise CrossingEntryException(message)
        super(Record, self).save(*agrs, **kwargs)
