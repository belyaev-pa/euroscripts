from django.conf.urls import url
from .views import *
app_name = 'polls'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^scheme_upload/$', scheme_upload, name='scheme_upload'),
    url(r'^result_upload/$', result_upload, name='result_upload'),
    url(r'^report/$', report, name='report'),
]