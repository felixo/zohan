# -*- coding: utf-8 -*-
import datetime

from django.core.exceptions import ValidationError
from django.core.validators import email_re
from settings_local import DEBUG
from django import forms

from models import Record
from metro import METRO_CHOICES


def send_email(address, name, start, end, service):
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
    attendees = [address]
    organizer = "ORGANIZER;CN=Deemaz:mailto:calendar@deemaz.ru"
    fro = "Deemaz <calendar@deemaz.ru>"
    deemaz = 'alexei.eremin@gmail.com' if DEBUG else 'calendar@deemaz.ru'

    ddtstart = start
    dur = end - start
    ddtstart = ddtstart
    dtend = ddtstart + dur
    dtstamp = str(datetime.datetime.now().strftime("%Y%m%dT%H%M%S+0300"))
    dtstart = str(ddtstart.strftime("%Y%m%dT%H%M%S+0300"))
    dtstartx = str(ddtstart.strftime("%Y-%m-%d %H:%M"))
    dtend = str(dtend.strftime("%Y%m%dT%H%M%S+0300"))

    description = u"DESCRIPTION: Deemaz" + service + CRLF
    description_deemaz = u"DESCRIPTION:" + name + u" " + service + CRLF
    attendee = ""
    for att in attendees:
        attendee += "ATTENDEE;UTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"+CRLF+" ;CN="+att+";X-NUM-GUESTS=0:"+CRLF+" mailto:"+att+CRLF
    ical = "BEGIN:VCALENDAR"+CRLF+"PRODID:pyICSParser"+CRLF+"VERSION:2.0"+CRLF+"CALSCALE:GREGORIAN"+CRLF
    ical+="METHOD:REQUEST"+CRLF+"BEGIN:VEVENT"+CRLF+"DTSTART:"+dtstart+CRLF+"DTEND:"+dtend+CRLF+"DTSTAMP:"+dtstamp+CRLF+organizer+CRLF
    ical+= "UID:UUUUU"+dtstamp+CRLF
    ical+= attendee+"CREATED:"+dtstamp+CRLF+description+"LAST-MODIFIED:"+dtstamp+CRLF+"LOCATION:"+CRLF+"SEQUENCE:0"+CRLF+"STATUS:CONFIRMED"+CRLF
    ical+= u"SUMMARY:Deemaz "+service+CRLF+"TRANSP:OPAQUE"+CRLF+"END:VEVENT"+CRLF+"END:VCALENDAR"+CRLF

    ical_deemaz = "BEGIN:VCALENDAR" + CRLF + "PRODID:pyICSParser" + CRLF + "VERSION:2.0" + CRLF + "CALSCALE:GREGORIAN" + CRLF
    ical_deemaz += "METHOD:REQUEST" + CRLF + "BEGIN:VEVENT" + CRLF + "DTSTART:" + dtstart + CRLF + "DTEND:" + dtend + CRLF + "DTSTAMP:" + dtstamp + CRLF + organizer + CRLF
    ical_deemaz += "UID:UUUUU" + dtstamp + CRLF
    ical_deemaz += attendee + "CREATED:" + dtstamp + CRLF + description_deemaz + "LAST-MODIFIED:" + dtstamp + CRLF + "LOCATION:" + CRLF + "SEQUENCE:0" + CRLF + "STATUS:CONFIRMED" + CRLF
    ical_deemaz += u"SUMMARY:" + name + u" " + service + CRLF + "TRANSP:OPAQUE" + CRLF + "END:VEVENT" + CRLF + "END:VCALENDAR" + CRLF

    eml_body = u"Приглашение на стрижку: " + name + ", " + dtstartx
    eml_body_deemaz = u"Информация о стрижке: " + name + u" " + service
    msg = MIMEMultipart('mixed')
    msg_deemaz = MIMEMultipart('mixed')
    msg['Reply-To']=fro
    msg_deemaz['Reply-To']=fro
    msg['Date'] = formatdate(localtime=True)
    msg_deemaz['Date'] = formatdate(localtime=True)
    msg['Subject'] = (service + u" " + dtstartx).encode('utf-8')
    msg_deemaz['Subject'] = (name + u" " + service).encode('utf-8')
    msg['From'] = fro
    msg_deemaz['From'] = fro
    msg['To'] = ",".join(attendees)
    msg_deemaz['To'] = ",".join([deemaz])

    part_email = MIMEText(eml_body.encode('utf-8'), "html", "utf-8")
    part_email_deemaz = MIMEText(eml_body_deemaz.encode('utf-8'), "html", "utf-8")
    part_cal = MIMEText(ical,'calendar;method=REQUEST', "utf-8")
    part_cal_deemaz = MIMEText(ical_deemaz, 'calendar;method=REQUEST', "utf-8")

    msgAlternative = MIMEMultipart('alternative')
    msgAlternativeD = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    msg_deemaz.attach(msgAlternativeD)

    ical_atch = MIMEBase('application/ics',' ;name="%s"'%("invite.ics"))
    ical_atch_deemaz = MIMEBase('application/ics', ' ;name="%s"' % ("invite.ics"))
    ical_atch.set_payload(ical.encode('utf-8'))
    ical_atch_deemaz.set_payload(ical.encode('utf-8'))
    Encoders.encode_base64(ical_atch)
    Encoders.encode_base64(ical_atch_deemaz)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"'%("invite.ics"))
    ical_atch_deemaz.add_header('Content-Disposition', 'attachment; filename="%s"' % ("invite.ics"))

    eml_atch = MIMEBase('text/plain','')
    Encoders.encode_base64(eml_atch)
    eml_atch.add_header('Content-Transfer-Encoding', "")

    msgAlternative.attach(part_email)
    msgAlternativeD.attach(part_email_deemaz)

    msgAlternative.attach(part_cal)
    msgAlternativeD.attach(part_cal_deemaz)

    mailServer = smtplib.SMTP('smtp.locum.ru', 25)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(login, password)
    mailServer.sendmail(fro, attendees, msg.as_string())
    mailServer.sendmail(fro, [deemaz], msg_deemaz.as_string())
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
        service = []
        if record.man_haircut:
            print record
            service.append(u'Мужская стрижка')
        if record.woman_haircut:
            service.append(u'Женская стрижка')
        if record.coloring:
            service.append(u'Окрашивание')
        if record.haircare:
            service.append(u'Уход')
        if record.laminate:
            service.append(u'Ламинирование')
        if record.catering:
            service.append(u'Выезд')
        calendar_service = u'+'.join(service)
        try:
            send_email(record.email, record.name, record.start, record.end, calendar_service)
        except:
            import traceback
            open('/tmp/axz', 'a').write(traceback.format_exc() + '\n\n\n')
        return record


    def save_no_email(self, *args,**kwargs):
        record = super(RecordForm, self).save(commit=False, *args, **kwargs)
        record.updateTime()
        service = []
        if record.man_haircut:
            print record
            service.append(u'Мужская стрижка')
        if record.woman_haircut:
            service.append(u'Женская стрижка')
        if record.coloring:
            service.append(u'Окрашивание')
        if record.haircare:
            service.append(u'Уход')
        if record.laminate:
            service.append(u'Ламинирование')
        if record.catering:
            service.append(u'Выезд')
        calendar_service = u'+'.join(service)
        return record