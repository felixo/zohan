# Encoding: utf-8
import datetime
from django.contrib.auth.decorators import login_required
from common.decorators import render_to
from dateutil.relativedelta import relativedelta
from django_settings.models import Setting

from record.forms import RecordForm
from record.models import Record

@render_to('index.html')
def index(request):

    form = RecordForm()

    return {
        'form': form,
        'greetings': Setting.objects.get_value('greetings', default=u'Привет')
    }


@login_required
@render_to('mobile_content.html')
def get_mobile_content(request):
    records = Record.objects.filter(start__range=(datetime.date.today(), (datetime.date.today() + relativedelta(days=1)))).order_by('start')
    return {
        'records': records,
        'today': datetime.date.today()
    }