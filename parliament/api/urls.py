from django.conf.urls import url

from . import views

app_name = 'api'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.users, name='users'),
    url(r'^create_conference/$', views.create_conference, name='create_conference'),
    url(r'^akti/$', views.akti, name='akti'),  #pretraga, gadja je AllActsController
    url(r'^(?P<uri>)/pdf/$', views.aktPdf, name='pdf'), #ako treba regex za ovo uri stavite
    url(r'^(?P<uri>)/xml/$', views.aktXml, name='xml'),
    url(r'^(?P<uri>)/html/$', views.aktHtml, name='html'),

]