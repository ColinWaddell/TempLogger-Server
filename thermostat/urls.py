from django.conf.urls import url

from . import views

app_name = 'thermostat'
urlpatterns = [
    url(r'^events/days/(?P<ago>[0-9]+)/$', views.events, {"units": "days"}, name='events'),
    url(r'^events/weeks/(?P<ago>[0-9]+)/$', views.events, {"units": "weeks"}, name='events'),
    url(r'^events/$', views.events, name='events')
]