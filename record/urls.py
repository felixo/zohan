from django.conf.urls.defaults import *

from record import views

urlpatterns = patterns('',
    (r'^save/(?P<id>\d+)/$', views.save),
    (r'^save/$', views.save),
    (r'^list/$', views.list),
    (r'^delete/$', views.delete),
    (r'^get_day_status/$', views.get_day_status),
    (r'^set_day_status/$', views.set_day_status),
    (r'^resize/(?P<id>\d+)/$', views.resize),
)