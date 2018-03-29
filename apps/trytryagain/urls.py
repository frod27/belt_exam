from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.preindex),
    url(r'^main$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^landing$', views.landing),
	url(r'^join/(?P<id>\d+)$', views.join),
	url(r'^remove/(?P<id>\d+)$', views.remove),
	url(r'^landing/add$', views.add),
	url(r'^addItem$', views.addItem),
	url(r'^landing/item/(?P<id>\d+)$', views.item)
]
