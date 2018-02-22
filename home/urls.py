from django.conf.urls import include, url
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.views.generic import RedirectView
from django.contrib import admin
#----------URL'S AVAILABLE AFTER LOGIN- NON USER MODEL RELATED-------------
# admin.autodiscover()
app_name = 'home'

urlpatterns = [
                  path('', views.home, name='home'),
                  url(r'^reports/$', views.reports, name='reports'),
                  url(r'^reports/clear/$', views.reports_clear, name='reports_clear'),
                  url(r'^reports/(?P<id>\d+)/$', views.reports_specified, name='reports_specified'),
                  url(r'^reports/(?P<id>\d+)/clear/$', views.reports_specified_clear, name='reports_specified_clear'),
                  url(r'^ownfiles/$', views.ownfiles, name='ownfiles'),
                  url(r'^group_list/$', views.group_list, name='group_list'),
                  url(r'^group_register/$', views.group_register, name='group_register'),
                  url(r'^group_list/(?P<id>\d+)/$', views.group_detail, name='group_detail'),
                  url(r'^group_list/(?P<id>\d+)/edit/$', views.group_edit, name='group_edit'),
                  url(r'^group_list/(?P<id>\d+)/delete/$', views.group_delete, name='group_delete'),
                  url(r'^group_list/(?P<id>\d+)/comment/$', views.group_detail_comment, name='group_detail_comment'),
                  url(r'^group_list/(?P<id>\d+)/(?P<idc>\d+)/delete/$', views.group_detail_comment_delete,
                      name='group_detail_comment_delete'),
                  url(r'^group_list/(?P<id>\d+)/files/$', views.group_detail_files, name='group_detail_files'),
                  url(r'^group_list/(?P<id>\d+)/files/upload/$', views.group_detail_files_upload,
                      name='group_detail_files_upload'),
                  url(r'^group_list/(?P<id>\d+)/files/(?P<idf>\d+)/comment/$', views.group_detail_files_comment,
                      name='group_detail_files_comment'),
                  url(r'^group_list/(?P<id>\d+)/files/(?P<idf>\d+)/(?P<idc>\d+)/delete/$',
                      views.group_detail_files_comment_delete, name='group_detail_files_comment_delete'),
                  url(r'^group_list/(?P<id>\d+)/files/(?P<idf>\d+)/delete/$', views.group_detail_files_delete,
                      name='group_detail_files_delete'),
                  url(r'^group_list/(?P<id>\d+)/files/(?P<idf>\d+)/download/$', views.group_detail_files_download,
                      name='group_detail_files_download'),

                  url(r'^prompt/duplicate/$', views.prompt_duplicate, name='prompt_duplicate'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
