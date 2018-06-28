# -*- coding: utf-8 -*-
import datetime

from django.core.exceptions import ValidationError
from django.core.validators import email_re
from django import forms

from models import Record
from metro import METRO_CHOICES


def send_email(address, name, start, end):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.Utils import COMMASPACE, formatdate
    from email import Encoders
    import os,datetime

    CRLF = "\r\n"
    login = "calendar@deemaz.ru"
    password = "LeninaL14"
    attendees = ["calendar@deemaz.ru", address]
    organizer = "ORGANIZER;CN=Deemaz:mailto:calendar@deemaz.ru"
    fro = "Deemaz <calendar@deemaz.ru>"

    ddtstart = start
    dur = end - start
    ddtstart = ddtstart
    dtend = ddtstart + dur
    dtstamp = str(datetime.datetime.now().strftime("%Y%m%dT%H%M%S+0300"))
    dtstart = str(ddtstart.strftime("%Y%m%dT%H%M%S+0300"))
    dtstartx = str(ddtstart.strftime("%Y-%m-%d %H:%M"))
    dtend = str(dtend.strftime("%Y%m%dT%H%M%S+0300"))

    description = u"DESCRIPTION: Стрижка (" + name + ") " + dtstartx + CRLF
    attendee = ""
    for att in attendees:
        attendee += "ATTENDEE;UTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
    ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
    ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
    ical+= "UID:UUUUU"+dtstamp+CRLF
    ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
    ical+= u"SUMMARY:Стрижка "+dtstartx+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF

    eml_body = eml_body_bin = u"Приглашение на стрижку: " + name + ", " + dtstartx
    msg = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = (u"Стрижка (" + name + u") — " + dtstartx).encode('utf-8')
    msg['From'] = fro
    msg['To'] = ",".join(attendees)

    part_email = MIMEText(eml_body.encode('utf-8'), "html", "utf-8")
    part_cal = MIMEText(ical,'calendar;method=REQUEST', "utf-8")

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
    ical_atch.set_payload(ical.encode('utf-8'))
    Encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))

    eml_atch = MIMEBase('text/plain','')
    Encoders.encode_base64(eml_atch)
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msgAlternative.attach(part_email)
    msgAlternative.attach(part_cal)

    mailServer = smtplib.SMTP('smtp.locum.ru', 25)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(login, password)
    mailServer.sendmail(fro, attendees, msg.as_string())
    mailServer.close()


class RecordForm(forms.ModelForm):
    start = forms.CharField(widget=forms.HiddenInput())
    end = forms.CharField(widget=forms.HiddenInput(), required=False)
    metro = forms.ChoiceField(widget=forms.Select, choices=METRO_CHOICES, label=u'Станция метро')

    class Meta:
        model = Record
        fields = ['name', 'catering', 'start', 'end', 'address', 'email', 'metro', 'man_haircut', 'woman_haircut', 'coloring', 'haircare', 'laminate']
        

    def __init__(self, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Ник и имя'
        self.fields['man_haircut'].label = 'Мужскую стрижку (1 час)'
        self.fields['woman_haircut'].label = 'Женскую стрижку (1.5 часа)'
        self.fields['coloring'].label = 'Окрашивание (1.5 часа)'
        self.fields['haircare'].label = 'Уход (30 мин)'
        self.fields['laminate'].label = 'Ламинирование (1 час)'

        self.fields['catering'].label = 'Нужен выезд на дом'
        self.fields['catering'].help_text = 'Запись сдвинется на полчаса назад.'

        self.fields['email'].label = 'Электронная почта'
        self.fields['email'].help_text = 'На почту придёт событие для Google‑календаря'

        self.fields['address'].label = 'Телефон и иные контактные данные и адрес (в случае выезда):'
        self.fields['address'].widget.attrs['style'] = ' '
        self.fields['address'].widget.attrs['rows'] = 4

        self.fields['metro'].required = False




    def clean_start(self):
        return datetime.datetime.fromtimestamp(int(self.cleaned_data['start'])/1000)

    def clean_end(self):
        end = self.cleaned_data['end']
        if end:
            return datetime.datetime.fromtimestamp(int(end)/1000)
        return None

    def clean_metro(self):
        metro = self.cleaned_data['metro'].strip()
        if self.cleaned_data['catering'] and not metro:
            raise ValidationError(u'Укажите станцию метро')
        return metro
        
    def clean(self):
        cd = self.cleaned_data
        if not (cd.get('man_haircut') or cd.get('woman_haircut') or cd.get('coloring') or cd.get('haircare') or cd.get('laminate')):
            self._errors["laminate"] = self.error_class([u'Выберите услугу'])
        if not email_re.match(cd.get('email', '')):
            self._errors["email"] = self.error_class([u'Введите действительный адрес'])
        return cd


    def save(self, *args, **kwargs):
        record = super(RecordForm, self).save(commit=False, *args, **kwargs)
        record.updateTime()
        try:
            send_email(record.email, record.name, record.start, record.end)
        except:
            import traceback
            open('/tmp/axz', 'a').write(traceback.format_exc() + '\n\n\n')
        return record
