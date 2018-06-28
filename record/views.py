# Encoding: utf-8
import time
import datetime
from django.contrib.auth.decorators import login_required

from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson
from dateutil import relativedelta

from forms import RecordForm
from models import Record, CrossingEntryException
from common.decorators import ajax, json, render_to
from record.models import DayStatus

json_serializer = serializers.get_serializer("json")()

@ajax
def save(request, id=None):
    if id is not None:
        if request.user.is_superuser:
            instance = Record.objects.get(id=id)
        else:
            instance = Record.objects.get(id=id, session_id=request.session.session_key)
        form = RecordForm(request.POST, instance=instance)
    else:
        form = RecordForm(request.POST)
    if not form.is_valid():
        return {
            'errors': form.errors
        }
    record = form.save()
    record.session_id = request.session.session_key
    try:
        record.save()
    except CrossingEntryException, e:
        return {
            'error': e.message,
        }        
    serialized_record = simplejson.loads(json_serializer.serialize([record], ensure_ascii=False))[0]['fields']
    #serialized_record['start'] = time.mktime(record.start.timetuple())*1000
    #serialized_record['end'] = time.mktime(record.end.timetuple())*1000
    serialized_record['start'] = time.strftime("%Y-%m-%dT%H:%M:%S", record.start.timetuple())
    serialized_record['end'] = time.strftime("%Y-%m-%dT%H:%M:%S", record.end.timetuple())
    serialized_record['title'] = record.get_title()
    serialized_record['id'] = record.id
    return {
        'record': serialized_record
    }

    
@json
def list(request):
    request.session.set_expiry(60 * 60 * 24 * 365) # Session will expiry after 100 days
    records = Record.objects.all().filter(start__gte=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(request.GET['start'])/1000)), \
                                            end__lte=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(request.GET['end'])/1000)))
    serialized_records = []
    for record in records:
        if record.session_id==request.session.session_key or request.user.is_superuser:
            serialized_record = simplejson.loads(json_serializer.serialize([record], ensure_ascii=False))[0]['fields']
            serialized_record['title'] = record.get_title()
            serialized_record['editable'] = True
            serialized_record['editable'] = True
        else:
            title = u'%s' % record.name
            if record.catering:
                if record.metro:
                    title = u'%s, м.%s' % (title, record.metro)
            serialized_record = {
                'title': title,
                'editable': False,
                'resizable': False,
            }
        #serialized_record['start'] = time.mktime(record.start.timetuple())*1000
        #serialized_record['end'] = time.mktime(record.end.timetuple())*1000
	serialized_record['start'] = time.strftime("%Y-%m-%dT%H:%M:%S", record.start.timetuple())
	serialized_record['end'] = time.strftime("%Y-%m-%dT%H:%M:%S", record.end.timetuple())
        serialized_record['catering'] = record.catering
        serialized_record['metro'] = record.metro
        serialized_record['id'] = record.id
        serialized_records.append(serialized_record)

    return {
        'records': serialized_records
    }

@ajax
def delete(request):
    id = int(request.POST.get('id', 0))
    Record.objects.filter(id=id).delete()
    return {
        'status': 'OK'
    }


@ajax
def get_day_status(request):
    return HttpResponse(DayStatus.get_status_for_day(request.POST.get('date')))

@ajax
def set_day_status(request):
    if not request.user.is_superuser:
        return HttpResponse('Trololo')
    try:
        ds = DayStatus.objects.get(date=request.POST.get('date'))
    except DayStatus.DoesNotExist:
        ds = DayStatus(date=request.POST.get('date'))
    ds.status=request.POST.get('status')
    ds.save()
    return HttpResponse(ds.get_status_display())

