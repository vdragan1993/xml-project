from django.conf.urls import url

from . import views

app_name = 'api'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.users, name='users'),
    url(r'^create_conference/$', views.create_conference, name='create_conference'),
    url(r'^create_act/$', views.create_act, name='create_act'),
    url(r'^create_amendment/$', views.create_amendment, name='create_amendment'),
    url(r'^simple_search/$', views.simple_search, name='simple_search'),
    url(r'^akti/$', views.akti, name='akti'),  #pretraga, gadja je AllActsController
    url(r'^pdf/$', views.aktPdf, name='pdf'), #ako treba regex za ovo uri stavite
    url(r'^xml/$', views.aktXml, name='xml'),
    url(r'^html/$', views.aktHtml, name='html'),
    url(r'^svi/$', views.get_all, name='svi')

]