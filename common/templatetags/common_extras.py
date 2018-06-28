# -*- coding: utf-8
import os

from django import template
from django.utils.encoding import smart_unicode
import settings

register = template.Library()

@register.inclusion_tag('common/link.html')
def link(object, anchor=u'', postfix1='', postfix2=''):
    """
    Return A tag with link to object.
    """
    user_id = None
    url = (hasattr(object,'get_absolute_url') and object.get_absolute_url() or '') + postfix1 + postfix2
    anchor = anchor or smart_unicode(object)
    return {'user_id': user_id,
            'url': url,
            'anchor': anchor}



@register.simple_tag
def GOOGLE_MAPS_API_KEY():
    return settings.GOOGLE_MAPS_API_KEY

@register.simple_tag
def MEDIA_URL():
    return settings.MEDIA_URL

@register.simple_tag
def REVISION():
    return settings.REVISION