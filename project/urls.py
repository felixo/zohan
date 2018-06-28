from django.conf.urls.defaults import *

from project import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^m/$', views.get_mobile_content),
)