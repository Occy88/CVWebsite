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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)