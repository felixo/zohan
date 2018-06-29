from django.conf.urls.defaults import *

from project import views

urlpatterns = patterns('',
    (r'^$', views.index),
    (r'^m/$', views.get_mobile_content),
    (r'yandex_d24aa8e1eb7bf7be.html/$', views.yandex_content),
)