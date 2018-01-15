from django.conf.urls import url

from . import views

app_name = 'thermostat'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^noscript', views.index, name='noscript', kwargs={"noscript": True}),
    url(r'^status/$', views.status, name='status'),
    url(r'^boost/(?P<thermostat_id>[0-9]+)/(?P<hours>[0-9]+)/$', views.boost, name='boost'),
    url(r'^mode/(?P<thermostat_id>[0-9]+)/(?P<mode>[\w\-\ ]+)/$', views.mode, name='mode'),
    url(r'^jog_target/(?P<thermostat_id>[0-9]+)/(?P<delta>[-?\d+]+)/$', views.jog_target, name='jog_target'),
]