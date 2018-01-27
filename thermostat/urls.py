from django.conf.urls import url

from . import views

app_name = 'thermostat'
urlpatterns = [
    url(r'^events/(?P<thermostat_id>[0-9]+)/days/(?P<ago>[0-9]+)/$', views.events, {"units": "days"}, name='events'),
    url(r'^events/(?P<thermostat_id>[0-9]+)/weeks/(?P<ago>[0-9]+)/$', views.events, {"units": "weeks"}, name='events')
]