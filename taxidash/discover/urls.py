from django.conf.urls import url

from . import views

app_name = 'discover'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^join/$', views.join, name='join'),
    url(r'^organize/$', views.organize, name='organize'),
    url(r'^createTrip/$', views.createTrip, name='createTrip'),
]
