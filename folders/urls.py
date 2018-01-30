from django.urls import path
from django.conf.urls import url

from . import views
app_name='folders'
urlpatterns = [
    #/files/
    path('', views.folders, name='folders'),
    #/files/documents
    url(r'^(?P<folder_id>[0-9]+)/$', views.detail, name='detail'),

    url(r'^(?P<folder_id>[0-9]+)/favorite/$', views.favorite, name='favorite')
]