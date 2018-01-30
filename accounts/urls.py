from django.urls import path
from django.conf.urls import url
from  django.contrib.auth.views import login

from . import views
app_name='accounts'
urlpatterns = [
    #/files/
    path('', views.home, name='accounts'),
    url(r'^login/$',login,{'template_name':'accounts/templates/accounts/login.html'}),
    url(r'^register/$',views.register,name='register'),
    url(r'^logout/$',login,{'template_name':'accounts/templates/accounts/logout.html'})
    #/files/documents

]