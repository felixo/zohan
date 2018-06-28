# -*- coding: utf-8 -*-
from datetime import datetime
import os.path
import random
import traceback
import logging

from django.shortcuts import render_to_response
from django.template import RequestContext

from common.http import HttpResponseJson, HttpResponseDenied

def render_to(template_path):
    """
    Expect the dict from view. Render returned dict with
    RequestContext.
    """

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            import pdb
            #output = pdb.runcall(func, request, *args, **kwargs)
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            kwargs = {'context_instance': RequestContext(request)}
            if 'MIME_TYPE' in output:
                kwargs['mimetype'] = output.pop('MIME_TYPE')
            if 'TEMPLATE' in output:
                template = output.pop('TEMPLATE')
            else:
                template = template_path
            started = datetime.now()
            resp = render_to_response(template, output, **kwargs)
            #logging.debug('Rendered in %s' % str(datetime.now() - started))
            if 'COOKIES' in output:
                cookies = output.pop('COOKIES')
                for item in cookies:
                    resp.set_cookie(*item)
            return resp

        return wrapper

    return decorator


class JsonError(Exception):
    pass

def ajax(func):
    """
    Wrap response of view into JSON format.

    Checks request.method is POST. Return error in JSON in other case.
    """

    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            try:
                response = func(request, *args, **kwargs)
            except JsonError, ex:
                response = {'error': unicode(ex.message)}
            except Exception, ex:
                logging.error(traceback.format_exc())
                response = {'error': traceback.format_exc()}
                print traceback.format_exc()
        else:
            response = {'error': {'type': 403, 'message': 'Accepts only POST request'}}
        if isinstance(response, dict):
            try:
                return HttpResponseJson(response)
            except Exception, ex:
                print 'JSON error:', ex
                return HttpResponseJson({'error': 'Could not serialize the data.'})
        else:
            return response
    return wrapper
    


def json(func):
    """
    Wrap response of view into JSON format.

    Instead of @ajax it doesn't checks request.method is POST.
    """

    def wrapper(request, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
        except Exception, ex:
            response = {'error': traceback.format_exc()}
        if isinstance(response, dict):
            try:
                return HttpResponseJson(response)
            except Exception, ex:
                print 'JSON error:', ex
                return HttpResponseJson({'error': 'Could not serialize the data.'})
        else:
            return response
    return wrapper