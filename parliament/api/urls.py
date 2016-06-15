from django.conf.urls import url

from . import views

app_name = 'api'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.users, name='users'),
    url(r'^logout/$', views.logout, name='logout'),
]