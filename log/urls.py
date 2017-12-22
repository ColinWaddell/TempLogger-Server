from django.conf.urls import url

from . import views

app_name = 'log'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<weeks_ago>[0-9]+)/$', views.index, name='index'),
    url(r'^get/(?P<weeks_ago>[0-9]+)/$', views.get, name='get'),
    url(r'^get/$', views.get, name='get'),
    url(r'^update/(?P<sensor_id>[0-9]+)/(?P<temperature_c>[-+]?[0-9]*\.?[0-9]+)/$', views.update, name='update'),
]