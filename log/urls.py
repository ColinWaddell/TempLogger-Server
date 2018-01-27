from django.conf.urls import url

from . import views

app_name = 'log'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^days/$', views.index, {"units": "days"}, name='index'),
    url(r'^days/(?P<ago>[0-9]+)/$', views.index, {"units": "days"}, name='index'),
    url(r'^get/weeks/(?P<ago>[0-9]+)/$', views.get, {"units": "weeks"}, name='get'),
    url(r'^get/days/(?P<ago>[0-9]+)/$', views.get, {"units": "days"}, name='get'),
    url(r'^get/$', views.get, name='get'),
    url(r'^update/(?P<sensor_id>[0-9]+)/(?P<temperature_c>[-+]?[0-9]*\.?[0-9]+)/$', views.update, name='update'),
]
