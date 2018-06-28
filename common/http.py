# -*- coding: utf-8 -*-


from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.utils import simplejson

class HttpResponseJson(HttpResponse):
    def __init__(self, data):
        json_data = simplejson.dumps(data)
        super(HttpResponseJson, self).__init__(
            content=json_data, mimetype='application/json')


class HttpResponseDenied(HttpResponseRedirect):
    """
    The response class for restricted requests.
    """

    def __init__(self):
        super(HttpResponseDenied, self).__init__(settings.LOGIN_URL)
        #self['Location'] = iri_to_uri(settings.LOGIN_URL)