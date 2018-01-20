from django.conf.urls import url

from . import views

app_name = 'thermostat'
urlpatterns = [
    url(r'^events/(?P<weeks_ago>[0-9]+)/$', views.events, name='events'),
    url(r'^events/$', views.events, name='events')
]