from django.conf.urls import url

from . import views

app_name = 'log'
urlpatterns = [
    url(r'^get/(?P<thermostat_id>[0-9]+)/weeks/(?P<ago>[0-9]+)/$', views.get, {"units": "weeks"}, name='get'),
    url(r'^get/(?P<thermostat_id>[0-9]+)/days/(?P<ago>[0-9]+)/$', views.get, {"units": "days"}, name='get'),
    url(r'^update/(?P<sensor_id>[0-9]+)/(?P<temperature_c>[-+]?[0-9]*\.?[0-9]+)/$', views.update, name='update'),
]
