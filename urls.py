from django.conf.urls.defaults import *
from django.contrib import admin
import django.views.static
import settings


admin.autodiscover()

import settings


urlpatterns = patterns('',
    (r'^', include('project.urls')),
    (r'^record/', include('record.urls')),


    (r'^admin/', include(admin.site.urls)),

    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
       django.views.static.serve, {'document_root': settings.MEDIA_ROOT}),
    
)
