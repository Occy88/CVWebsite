from django.conf.urls import  include, url
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.views.generic import RedirectView
from django.contrib import admin
# admin.autodiscover()
app_name='home'

urlpatterns = [
    path('', views.list, name='home'),
    url(r'^list/$', views.list, name='list'),
    url(r'^group_list/$', views.group_list, name='group_list'),
    url(r'^group_register/$',views.group_register,name='group_register'),
    url(r'^group_list/(?P<id>\d+)/edit/$', views.group_edit, name='group_edit'),
    url(r'^group_list/(?P<id>\d+)/$', views.group_detail, name='group_detail'),
    url(r'^group_list/(?P<id>\d+)/delete$', views.group_delete, name='group_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)